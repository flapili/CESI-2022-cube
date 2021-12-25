# coding: utf-8
import hashlib
import datetime
from typing import Optional
from pathlib import Path
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

import requests
from jose import jwt, exceptions as jose_exceptions
from fastapi import HTTPException, status, Security, Depends
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader
from fastapi.templating import Jinja2Templates

# from pydantic import BaseModel
from sqlmodel import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

import db
from settings import get_settings


settings = get_settings()
engine = create_async_engine(
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password.get_secret_value()}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}"
)
templates = Jinja2Templates(directory="templates")


def get_templates() -> Jinja2Templates:
    return templates


def hash_password(password: str) -> str:
    temp_hash = password
    for _ in range(10000):
        temp_hash = hashlib.sha512(temp_hash.encode("utf-8")).hexdigest()
    return temp_hash


async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session


def resolve_path(file):
    routes_path = Path(__file__).resolve().parent / "routes"

    relative_path = Path("/") / Path(file).resolve().parent.relative_to(routes_path)
    return str(relative_path).replace("\\", "/")


def send_mail(to: str, content_html: str, subject: str, sender: str = settings.mailjet_sender_email):
    data = {
        "Messages": [
            {
                "From": {"Email": sender, "Name": settings.mailjet_sender_name},
                "To": [{"Email": to}],
                "Subject": subject,
                "HTMLPart": content_html,
            }
        ]
    }
    requests.post(
        "https://api.mailjet.com/v3.1/send",
        json=data,
        auth=(settings.mailjet_apikey_public.get_secret_value(), settings.mailjet_apikey_private.get_secret_value()),
    )


def get_jwt_token(
    jwt_token_query: Optional[str] = Security(APIKeyQuery(name="token", auto_error=False)),
    jwt_token_header: Optional[str] = Security(APIKeyHeader(name="token", auto_error=False)),
    jwt_token_cookie: Optional[str] = Security(APIKeyCookie(name="token", auto_error=False)),
) -> str:
    token: Optional[str] = jwt_token_query or jwt_token_header or jwt_token_cookie
    if token is not None:
        return token
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")


class JWTBody(BaseModel):
    email: EmailStr
    user_id: int
    iat: datetime.datetime
    exp: datetime.datetime


def get_jwt_body(token: str = Depends(get_jwt_token)) -> JWTBody:
    try:
        body = jwt.decode(token, settings.jwt_secret.get_secret_value(), algorithms="HS256")
        return JWTBody(**body)
    except jose_exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail={"message": "invalid token (too old)"})
    except jose_exceptions.JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "invalid token"})


async def get_user(
    jwt_body: JWTBody = Depends(get_jwt_body),
    session: AsyncSession = Depends(get_session),
) -> db.User:
    query = select(db.User).where(db.User.id == jwt_body.user_id).limit(1)
    user_result = await session.execute(query)
    user: db.User = user_result.scalar()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "user not found, try relogin"})

    if user.disabled_at is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"message": "user disabled"})

    return user

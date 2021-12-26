# coding: utf-8
import time
import datetime
from typing import Optional

import premailer
from pydantic import BaseModel, constr, EmailStr
from sqlmodel import select, update, func
from jose import jwt, exceptions as jose_exceptions
from fastapi import Depends, HTTPException, status, APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

import db
from settings import get_settings, Settings
from utils import get_session, AsyncSession, send_mail, hash_password, get_templates


router = APIRouter()


@router.get("/verify_token")
async def get_verify_token(
    token: str,
    settings: Settings = Depends(get_settings),
    session: AsyncSession = Depends(get_session),
):
    try:
        body = jwt.decode(token, settings.jwt_secret.get_secret_value(), algorithms="HS256")
    except jose_exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail={"message": "invalid token (too old)"})
    except jose_exceptions.JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "invalid token"})

    query = select(db.User).where(db.User.email == body["email"])
    user_res = await session.execute(query)
    user: Optional[db.User] = user_res.scalar()
    if user.credential_updated_at.timestamp() > body["iat"]:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={"message": "invalid token (credentials updated after the creation of this token)"},
        )

    return True


class PostBody(BaseModel):
    token: str
    password: constr(min_length=8)


@router.post("")
async def post(
    body: PostBody,
    settings: Settings = Depends(get_settings),
    session: AsyncSession = Depends(get_session),
):
    try:
        jwt_body = jwt.decode(body.token, settings.jwt_secret.get_secret_value(), algorithms="HS256")
    except jose_exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail={"message": "invalid token (too old)"})
    except jose_exceptions.JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "invalid token"})

    query = (
        update(db.User)
        .values(hashed_password=hash_password(body.password), credential_updated_at=func.now())
        .where(db.User.email == jwt_body["email"])
        .where(db.User.credential_updated_at < datetime.datetime.fromtimestamp(jwt_body["iat"]))
    )
    print(query)
    res = await session.execute(query)
    await session.commit()
    if res.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={"message": "invalid token (credentials updated after the creation of this token)"},
        )
    return {"message": "password changed"}


class PostSendMailBody(BaseModel):
    email: EmailStr


class PostSendMailResponse202(BaseModel):
    message: str


@router.post(
    "/send_mail",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {
            "model": PostSendMailResponse202,
            "description": "Lien envoyé par email",
            "content": {"application/json": {"example": {"message": "link sent by email"}}},
        },
    },
)
async def post_send_mail(
    body: PostSendMailBody,
    tasks: BackgroundTasks,
    settings: Settings = Depends(get_settings),
    session: AsyncSession = Depends(get_session),
    templates: Jinja2Templates = Depends(get_templates),
):
    """Envoie un mail de réinitialisation de mot de passe."""
    query = select(db.User).where(db.User.email == body.email).limit(1)
    user_res = await session.execute(query)
    user: db.User = user_res.scalar()
    if user is None:
        # don't leak if email already exists or not to avoid email spoofing
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "link sent by email"})

    now = time.time()
    jwt_body = {
        "email": user.email,
        "iat": now,
        "exp": now + 60 * 60,  # valid 1 hour
    }
    jwt_token = jwt.encode(jwt_body, settings.jwt_secret.get_secret_value(), algorithm="HS256")
    reset_link = f"{settings.front_deployment_domain}/reset_password?token={jwt_token}"
    template = templates.get_template("reset_password.html")
    content_html = template.render(reset_link=reset_link, api_base_url=settings.api_deployment_domain)
    content_html = premailer.transform(content_html)
    tasks.add_task(send_mail, to=body.email, content_html=content_html, subject="Réinitialisation de mot de passe")
    return {"message": "link sent by email"}

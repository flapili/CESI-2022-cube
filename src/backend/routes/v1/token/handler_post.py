# coding: utf-8
import datetime

from fastapi import FastAPI, Depends, HTTPException, status, Response
from pydantic import BaseModel, EmailStr
from sqlmodel import select
from jose import jwt

import db
from settings import Settings, get_settings
from utils import resolve_path, get_session, AsyncSession, hash_password


class Body(BaseModel):
    email: EmailStr
    password: str


def register_route(app: FastAPI):
    @app.post(resolve_path(__file__))
    async def route(
        body: Body,
        token_in_body: bool = False,
        settings: Settings = Depends(get_settings),
        session: AsyncSession = Depends(get_session),
    ):
        query = (
            select(db.User)
            .where(db.User.email == body.email)
            .where(db.User.hashed_password == hash_password(body.password))
        )
        user = await session.execute(query)
        user: db.User = user.scalar()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "bad credentials"})

        if user.disabled_at is not None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"message": "disabled user"})

        now = datetime.datetime.utcnow().timestamp()
        jwt_body = {
            "email": user.email,
            "user_id": user.id,
            "iat": now,
            "exp": now + 60 * 60 * 24 * 7,
        }
        jwt_token = jwt.encode(jwt_body, settings.jwt_secret.get_secret_value(), algorithm="HS256")

        if token_in_body is True:
            return {"token": jwt_token}
        else:
            response = Response()
            response.set_cookie(key="token", value=jwt_token)
            return response

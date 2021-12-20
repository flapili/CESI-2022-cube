# coding: utf-8
from fastapi import FastAPI, Depends, HTTPException, status
from jose import jwt, exceptions as jose_exceptions
from sqlalchemy import exc as sqlalchemy_exc


import db
from settings import get_settings, Settings
from utils import resolve_path, get_session, AsyncSession


def register_route(app: FastAPI):
    @app.get(resolve_path(__file__), status_code=status.HTTP_201_CREATED)
    async def route(
        token: str,
        settings: Settings = Depends(get_settings),
        session: AsyncSession = Depends(get_session),
    ):
        try:
            body = jwt.decode(token, settings.jwt_secret.get_secret_value(), algorithms="HS256")
        except jose_exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_410_BAD_REQUEST, detail={"message": "invalid token (too old)"})
        except jose_exceptions.JWTError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "invalid token"})

        user = db.User(**body)
        async with session.begin():
            session.add(user)
            try:
                await session.commit()
            except sqlalchemy_exc.IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail={"message": "email already used"}
                )  # TODO return on app

        return "created"  # TODO return on app

# coding: utf-8
import datetime

from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlmodel import select
from jose import jwt

import db
from settings import Settings, get_settings
from utils import resolve_path, get_session, AsyncSession, send_mail, get_templates, Jinja2Templates, hash_password


class Body(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str


def register_route(app: FastAPI):
    @app.post(resolve_path(__file__))
    async def route(
        body: Body,
        tasks: BackgroundTasks,
        settings: Settings = Depends(get_settings),
        session: AsyncSession = Depends(get_session),
        templates: Jinja2Templates = Depends(get_templates),
    ):
        query = select(1).select_from(db.User).where(db.User.email == body.email).exists().select()
        email_already_used = await session.execute(query)
        if email_already_used.scalar() is True:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"message": "Email already used"})

        now = datetime.datetime.utcnow().timestamp()
        jwt_body = {
            "firstname": body.firstname,
            "lastname": body.lastname,
            "email": body.email,
            "hashed_password": hash_password(body.password),
            "iat": now,
            "exp": now + 60 * 60 * 24,
        }
        jwt_token = jwt.encode(jwt_body, settings.jwt_secret.get_secret_value(), algorithm="HS256")
        activation_link = f"{settings.deployment_domain}/v1/register?token={jwt_token}"
        template = templates.get_template("welcome.html")
        content_html = template.render(lastname=body.lastname, activation_link=activation_link)
        tasks.add_task(send_mail, to=body.email, content_html=content_html, subject=f"Bienvenue {body.lastname}")
        return {"message": "invitation envoyé par email"}

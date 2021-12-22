# coding: utf-8
import datetime
from pathlib import Path
from typing import Optional

import premailer
from pydantic import BaseModel, EmailStr, constr
from PIL import Image, UnidentifiedImageError
from sqlmodel import select, update
from sqlalchemy import exc as sqlalchemy_exc
from jose import jwt, exceptions as jose_exceptions
from fastapi import Depends, HTTPException, status, APIRouter, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse, Response, FileResponse
from fastapi.templating import Jinja2Templates


import db
import const
from settings import get_settings, Settings
from utils import get_session, AsyncSession, send_mail, hash_password, get_templates, get_user


router = APIRouter()


class PostBody(BaseModel):
    firstname: constr(strip_whitespace=True, max_length=32)
    lastname: constr(strip_whitespace=True, max_length=32)
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=8)
    phone_number: constr(strip_whitespace=True, regex=const.PHONE_NUMBER_REGEX)


class PostResponse202(BaseModel):
    message: str


class PostResponse409(BaseModel):
    message: str


@router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {
            "model": PostResponse202,
            "description": "Invitation envoyé par email",
            "content": {"application/json": {"example": {"message": "Invitation sent by email"}}},
        },
        status.HTTP_409_CONFLICT: {
            "model": PostResponse409,
            "description": "L'Email est déjà utilisée",
            "content": {"application/json": {"example": {"message": "Email already used"}}},
        },
    },
)
async def post(
    body: PostBody,
    tasks: BackgroundTasks,
    settings: Settings = Depends(get_settings),
    session: AsyncSession = Depends(get_session),
    templates: Jinja2Templates = Depends(get_templates),
):
    """Envoie un mail d'inscription."""
    query = select(1).select_from(db.User).where(db.User.email == body.email).exists().select()
    email_already_used = await session.execute(query)
    if email_already_used.scalar() is True:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "Email already used"})

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
    activation_link = f"{settings.api_deployment_domain}/v1/user/register?incription_token={jwt_token}"
    template = templates.get_template("welcome.html")
    content_html = template.render(firstname=body.firstname, activation_link=activation_link)
    content_html = premailer.transform(content_html)
    tasks.add_task(send_mail, to=body.email, content_html=content_html, subject=f"Bienvenue {body.lastname}")
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Invitation sent by email"})


class GetMeResponse(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    phone_number: str
    created_at: datetime.datetime
    has_avatar: bool


@router.get("/me", response_model=GetMeResponse)
async def get_me(user: db.User = Depends(get_user)):
    """Retourne son profil utilisateur."""
    user = user.dict()
    user["has_avatar"] = bool(user["avatar_id"])
    return user


@router.get("/me/avatar")
async def get_me_avatar(
    me: db.User = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    if me.avatar_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    query = (
        select(db.Attachment)
        .select_from(db.User)
        .join(db.Attachment)
        .where(db.User.id == me.id)
        .where(db.Attachment.deleted_at == None)  # noqa
        .limit(1)
    )
    attachment_res = await session.execute(query)
    attachment: Optional[db.Attachment] = attachment_res.scalar()
    if attachment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return FileResponse(
        path=Path("attachments") / attachment.filename,
        media_type=f"image/{Path(attachment.name).suffix.lstrip('.')}",
    )


@router.post("/me/avatar")
async def post_me_avatar(
    avatar: UploadFile = File(...),
    me: db.User = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    """Permet d'éditer sa photo de profil."""
    if Path(avatar.filename).suffix not in (".png", ".jpeg"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad file extension")

    try:
        with Image.open(avatar.file) as im:
            width, height = im.size
            if width > 1024:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="width can't exceed 1024px"
                )

            if height > 1024:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="height can't exceed 1024px"
                )

            async with session.begin_nested() as tr:
                attachment = db.Attachment(name=avatar.filename)
                session.add(attachment)
                await tr.commit()

            await session.refresh(attachment)
            im.save(
                fp=Path("attachments") / attachment.filename,
                format=Path(attachment.name).suffix.lstrip("."),
            )

            async with session.begin_nested() as tr:
                query = update(db.User).where(db.User.id == me.id).values(avatar_id=attachment.id)
                await session.execute(query)
                await tr.commit()
            await session.commit()
            return {"message": "avatar changed"}

    except UnidentifiedImageError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad file")


class PostTokenBody(BaseModel):
    email: EmailStr
    password: str


@router.post("/token")
async def post_token(
    body: PostTokenBody,
    token_in_body: bool = False,
    settings: Settings = Depends(get_settings),
    session: AsyncSession = Depends(get_session),
):
    """Retourne un token d'authentification.
    - Si token_in_body = true => retourne le token dans le corps de la réponse
    - Sinon => assigne le token via un setCookie
    """
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


@router.get("/register", status_code=status.HTTP_201_CREATED)
async def get_register(
    incription_token: str,
    settings: Settings = Depends(get_settings),
    session: AsyncSession = Depends(get_session),
):
    """Permet de créer un utilisateur via un token JWT.<br>
    Ne devrait être appelé que par le lien du mail d'inscription.
    """
    try:
        body = jwt.decode(incription_token, settings.jwt_secret.get_secret_value(), algorithms="HS256")
    except jose_exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail={"message": "invalid token (too old)"})
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


class GetUserByIdResponse(BaseModel):
    firstname: str
    lastname: str
    created_at: datetime.datetime
    has_avatar: bool


@router.get("/{user_id}", dependencies=[Depends(get_user)], response_model=GetUserByIdResponse)
async def get_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Retourne un utilisateur donné."""
    user_res = await session.execute(select(db.User).where(db.User.id == user_id).limit(1))
    user: Optional[db.User] = user_res.scalar()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    user = user.dict()
    user["has_avatar"] = bool(user["avatar_id"])
    return user


@router.get("/{user_id}/avatar", dependencies=[Depends(get_user)])
async def get_by_id_avatar(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Retourne l'avatar d'un utilisateur donné."""
    query = (
        select(db.Attachment)
        .select_from(db.User)
        .join(db.Attachment)
        .where(db.User.id == user_id)
        .where(db.Attachment.deleted_at == None)  # noqa
        .limit(1)
    )
    attachment_res = await session.execute(query)
    attachment: Optional[db.Attachment] = attachment_res.scalar()
    if attachment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return FileResponse(
        path=Path("attachments") / attachment.filename,
        media_type=f"image/{Path(attachment.name).suffix.lstrip('.')}",
    )

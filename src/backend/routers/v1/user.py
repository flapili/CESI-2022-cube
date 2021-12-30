# coding: utf-8
import time
import zoneinfo
import datetime
from pathlib import Path
from typing import Optional, List

import premailer
from pydantic import BaseModel, EmailStr, constr, conint, PositiveInt
from PIL import Image, ExifTags, UnidentifiedImageError
from sqlmodel import select, update, or_, func
from sqlalchemy import exc as sqlalchemy_exc
from jose import jwt, exceptions as jose_exceptions
from fastapi import Depends, HTTPException, status, APIRouter, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse, Response, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


import db
import const
from settings import get_settings, Settings
from utils import (
    check_is_moderator,
    check_is_admin,
    get_session,
    AsyncSession,
    send_mail,
    hash_password,
    get_templates,
    get_user,
)


router = APIRouter()


class GetResponseUser(BaseModel):
    id: PositiveInt
    firstname: str
    lastname: str
    email: EmailStr
    phone_number: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    disabled_at: Optional[datetime.datetime]
    birthday: datetime.datetime
    type: str
    has_avatar: bool


class GetResponseMeta(BaseModel):
    page: PositiveInt
    per_page: PositiveInt
    total: conint(ge=0)


class GetResponse(BaseModel):
    users: List[GetResponseUser]
    meta: GetResponseMeta


@router.get("", dependencies=[Depends(check_is_moderator)], response_model=GetResponse)
async def get(
    page: PositiveInt = 1,
    session: AsyncSession = Depends(get_session),
):
    per_page: PositiveInt = 10
    async with session.begin_nested():
        query = select(db.User).offset((page - 1) * per_page).limit(per_page)
        users_res = await session.execute(query)
        query_total = select(func.count(db.User.id))
        total_user_res = await session.execute(query_total)
        users = [dict(u) for u in users_res.scalars()]

        for user in users:
            user["has_avatar"] = bool(user["avatar_id"])

        return {"users": users, "meta": {"page": page, "per_page": per_page, "total": total_user_res.scalar()}}


class PostBody(BaseModel):
    firstname: constr(strip_whitespace=True, max_length=32)
    lastname: constr(strip_whitespace=True, max_length=32)
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=8)
    phone_number: constr(strip_whitespace=True, regex=const.PHONE_NUMBER_REGEX)
    birthday: datetime.datetime


class PostResponse202(BaseModel):
    message: str


class PostResponse409(BaseModel):
    message: str


@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {
            "model": PostResponse202,
            "description": "Invitation envoyée par email",
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

    now = time.time()
    jwt_body = {
        "firstname": body.firstname,
        "lastname": body.lastname,
        "email": body.email,
        "phone_number": body.phone_number,
        "birthday": body.birthday.replace(tzinfo=zoneinfo.ZoneInfo("UTC")).isoformat(),
        "hashed_password": hash_password(body.password),
        "iat": now,
        "exp": now + 60 * 60 * 24,
    }
    jwt_token = jwt.encode(jwt_body, settings.jwt_secret.get_secret_value(), algorithm="HS256")
    activation_link = f"{settings.api_deployment_domain}/v1/user/register?incription_token={jwt_token}"
    template = templates.get_template("welcome.html")
    content_html = template.render(
        firstname=body.firstname, activation_link=activation_link, api_base_url=settings.api_deployment_domain
    )
    content_html = premailer.transform(content_html)
    tasks.add_task(send_mail, to=body.email, content_html=content_html, subject=f"Bienvenue {body.lastname}")
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Invitation sent by email"})


class GetMeResponse(BaseModel):
    id: PositiveInt
    firstname: str
    lastname: str
    email: EmailStr
    phone_number: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    birthday: datetime.datetime
    type: str
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
    ext = Path(avatar.filename).suffix.lower().lstrip(".")
    if ext == "jpg":
        ext = "jpeg"
    if ext not in ("png", "jpeg"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad file extension")

    try:
        with Image.open(avatar.file) as im:
            # im = ImageOps.contain(im, (1024, 1024))
            width, height = im.size
            if width > 1024 or height > 1024:
                im.thumbnail((1024, 1024))

            for orientation in ExifTags.TAGS:
                if ExifTags.TAGS[orientation] == "Orientation":
                    break

            exif = im._getexif()
            if exif is not None:
                if exif[orientation] == 3:
                    im = im.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    im = im.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    im = im.rotate(90, expand=True)

            async with session.begin_nested() as tr:
                attachment = db.Attachment(name=avatar.filename)
                session.add(attachment)
                await tr.commit()

            await session.refresh(attachment)
            im.save(fp=Path("attachments") / attachment.filename, format=ext)

            async with session.begin_nested() as tr:
                query = update(db.User).where(db.User.id == me.id).values(avatar_id=attachment.id)
                await session.execute(query)
                await tr.commit()
            await session.commit()
            return {"message": "avatar changed"}

    except UnidentifiedImageError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad file")


class PostLoginBody(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
async def post_login(
    body: PostLoginBody,
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

    now = time.time()
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
        response.set_cookie(key="token", value=jwt_token, httponly=True, samesite="None", secure=True)
        return response


@router.post("/logout")
async def post_logout(response: Response):
    response.set_cookie(key="token", value="", httponly=True, samesite="None", secure=True, max_age=0)


@router.get("/register")
async def get_register(
    incription_token: str,
    settings: Settings = Depends(get_settings),
):
    return RedirectResponse(f"{settings.front_deployment_domain}/welcome?token={incription_token}")


class PostRegisterBody(BaseModel):
    token: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def post_register(
    body: PostRegisterBody,
    settings: Settings = Depends(get_settings),
    session: AsyncSession = Depends(get_session),
):
    """Permet de créer un utilisateur via un token JWT.<br>
    Ne devrait être appelé que par le lien du mail d'inscription.
    """
    try:
        jwt_body = jwt.decode(body.token, settings.jwt_secret.get_secret_value(), algorithms="HS256")
    except jose_exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail={"message": "invalid token (too old)"})
    except jose_exceptions.JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "invalid token"})

    user = db.User(**jwt_body)
    firstname = user.firstname
    async with session.begin():
        session.add(user)
        try:
            await session.commit()
        except sqlalchemy_exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"message": "email already used"})

    return {"firstname": firstname}


class GetUserSearchResponseUser(BaseModel):
    id: PositiveInt
    firstname: str
    lastname: str
    created_at: datetime.datetime
    birthday: datetime.datetime
    type: str
    has_avatar: bool


class GetUserSearchResponse(BaseModel):
    users: List[GetUserSearchResponseUser]


@router.get("/search", response_model=GetUserSearchResponse)
async def get_search(
    query_search: str,
    session: AsyncSession = Depends(get_session),
    me: db.User = Depends(get_user),
):
    """Recherche les 10 premiers résultats d'une recherche dans le nom ou prénom"""
    query_search = query_search.lower()
    query = (
        select(db.User)
        .where(
            or_(
                func.lower(db.User.firstname).like(f"%{query_search}%"),
                func.lower(db.User.lastname).like(f"%{query_search}%"),
            )
        )
        .where(db.User.id != me.id)
        .where(db.User.disabled_at == None)  # noqa: E711
        .order_by(db.User.created_at)
        .limit(10)
    )
    users_res = await session.execute(query)
    users = [u.dict() for u in users_res.scalars().all()]
    for user in users:
        user["has_avatar"] = bool(user["avatar_id"])

    return {"users": users}


class GetUserByIdResponse(BaseModel):
    id: PositiveInt
    firstname: str
    lastname: str
    created_at: datetime.datetime
    birthday: datetime.datetime
    type: str
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


@router.post("/{user_id}/ban", dependencies=[Depends(check_is_moderator)])
async def ban_by_id(
    user_id: int,
    me: db.User = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    """Ban un utilisateur donné."""
    if me.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "can't ban yourself"})

    user_res = await session.execute(select(db.User).where(db.User.id == user_id).limit(1))
    user: Optional[db.User] = user_res.scalar()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    if user.disabled_at is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"message": "user already banned"})

    if user.type == db.UserType.admin:
        check_is_admin(me)

    query = update(db.User).values(disabled_at=func.now()).where(db.User.id == user_id)
    await session.execute(query)
    await session.commit()


@router.post("/{user_id}/unban", dependencies=[Depends(check_is_moderator)])
async def unban_by_id(
    user_id: int,
    me: db.User = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    """Unban un utilisateur donné."""
    user_res = await session.execute(select(db.User).where(db.User.id == user_id).limit(1))
    user: Optional[db.User] = user_res.scalar()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    if user.disabled_at is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"message": "user not banned"})

    if user.type == db.UserType.admin:
        check_is_admin(me)

    query = update(db.User).values(disabled_at=None).where(db.User.id == user_id)
    await session.execute(query)
    await session.commit()


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

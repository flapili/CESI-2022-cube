# coding: utf-8
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, conset
from sqlmodel import select, update, func, desc
from fastapi import Depends, File, HTTPException, UploadFile, status, APIRouter, BackgroundTasks, Form
# from fastapi.responses import JSONResponse

import db
# from settings import get_settings, Settings
from utils import get_session, AsyncSession, get_user


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def post(
    me: db.User = Depends(get_user),
    title: str = Form(...),
    type: Literal[
        "communication",
        "culture",
        "personal_development",
        "emotional_intelligence",
        "hobbie",
        "professional_world",
        "parenting",
        "quality_of_life",
        "search_of_meaning",
        "physical_health",
        "spirituality",
        "emotional_life",
    ] = Form(...),
    related: conset(
        Literal["itself", "spouse", "familly", "work", "friend_and_community", "everyone"],
        min_items=1,
    ) = Form(...),
    content: str = Form(...),
    attachment: Optional[UploadFile] = File(None),
    session: AsyncSession = Depends(get_session),
):
    """Crée un nouveau post (une ressource)"""
    async with session.begin_nested():
        if attachment is not None:
            db_attachment = db.Attachment(name=attachment.filename)
            session.add(db_attachment)
            await session.flush()
            await session.refresh(db_attachment)
            attachment_id = db_attachment.id
            with (Path("attachments") / attachment.filename).open(mode="wb") as f:
                f.write(await attachment.read())
        else:
            attachment_id = None

        post = db.Post(
            title=title,
            type=type,
            author_id=me.id,
            attachment_id=attachment_id,
            related_to_itself="itself" in related,
            related_to_spouse="spouse" in related,
            related_to_familly="familly" in related,
            related_to_work="work" in related,
            related_to_friend_and_community="friend_and_community" in related,
            related_to_everyone="everyone" in related,
            content=content,
        )
        session.add(post)
        await session.flush()
        await session.refresh(post)
        await session.commit()
    return "OK"


@router.get("")
async def get(
    session: AsyncSession = Depends(get_session),
):
    """Retourne tous les posts"""
    query = (
        select(db.Post, db.User)
        .join(db.User)
        .where(db.Post.deleted_at == None)  # noqa: E711
        .order_by(desc(db.Post.created_at))
    )
    results = await session.execute(query)
    return {
        "data": [
            {
                "post": r.Post,
                "author": {
                    "id": r.User.id,
                    "has_avatar": bool(r.User.avatar_id),
                    "firstname": r.User.firstname,
                    "lastname": r.User.lastname,
                },
            }
            for r in results
        ]
    }

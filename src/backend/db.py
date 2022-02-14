# coding: utf-8
import datetime
import enum
from uuid import uuid4
from typing import Optional

from pydantic import constr
from sqlmodel import Field, SQLModel, Column, DateTime, func, CheckConstraint, UniqueConstraint, Enum, Index

import const


class Base(SQLModel):
    __table_args__ = (CheckConstraint("created_at <= updated_at"),)

    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    )
    deleted_at: Optional[datetime.datetime] = Field(sa_column=Column(DateTime(timezone=True)))


class Attachment(Base, table=True):
    __tablename__ = "attachment"
    __table_args__ = (UniqueConstraint("filename"),)

    name: str = Field(nullable=False)
    filename: str = Field(nullable=False, default_factory=lambda: str(uuid4()))


class UserType(str, enum.Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"
    super_admin = "super admin"


class User(Base, table=True):
    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint("email"),
        UniqueConstraint("phone_number"),
        Index("ix_search_user_tsv", func.to_tsvector("english", "firstname || lastname"), postgresql_using="gin"),
    )

    firstname: constr(max_length=32) = Field(nullable=False)
    lastname: constr(max_length=32) = Field(nullable=False)
    email: str = Field(nullable=False)
    phone_number: constr(strip_whitespace=True, regex=const.PHONE_NUMBER_REGEX) = Field(nullable=False)
    birthday: datetime.datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    hashed_password: str = Field(nullable=False)
    avatar_id: Optional[int] = Field(foreign_key="attachment.id")
    disabled_at: Optional[datetime.datetime] = Field(sa_column=Column(DateTime(timezone=True)))
    credential_updated_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )
    type: UserType = Field(sa_column=Column(Enum(UserType), server_default=UserType.user, nullable=False))


class PostCategorie(str, enum.Enum):
    communication = "communication"
    culture = "culture"
    personal_development = "personal_development"
    emotional_intelligence = "emotional_intelligence"
    hobbie = "hobbie"
    professional_world = "professional_world"
    parenting = "parenting"
    quality_of_life = "quality_of_life"
    search_of_meaning = "search_of_meaning"
    physical_health = "physical_health"
    spirituality = "spirituality"
    emotional_life = "emotional_life"


class Post(Base, table=True):
    __tablename__ = "post"
    __table_args__ = (
        CheckConstraint(
            """
            related_to_itself OR
            related_to_spouse OR
            related_to_familly OR
            related_to_work OR
            related_to_friend_and_community OR
            related_to_everyone = TRUE
            """
        ),
    )

    title: str = Field(nullable=False)
    type: PostCategorie = Field(sa_column=Column(Enum(PostCategorie), nullable=False))
    author_id: int = Field(foreign_key="user.id", nullable=False)
    attachment_id: int = Field(foreign_key="attachment.id", nullable=True)
    related_to_itself: bool = Field(default=False)
    related_to_spouse: bool = Field(default=False)
    related_to_familly: bool = Field(default=False)
    related_to_work: bool = Field(default=False)
    related_to_friend_and_community: bool = Field(default=False)
    related_to_everyone: bool = Field(default=False)
    content: str = Field(nullable=False)


class UserHavePostInFavotite(Base, table=True):
    __tablename__ = "user_have_post_in_favorite"
    __table_args__ = (UniqueConstraint("user_id", "post_id", "deleted_at"),)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    post_id: int = Field(foreign_key="post.id", nullable=False)

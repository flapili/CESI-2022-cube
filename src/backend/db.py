# coding: utf-8
import datetime
from uuid import uuid4
from typing import Optional

from sqlmodel import Field, SQLModel, Column, DateTime, func, CheckConstraint, UniqueConstraint


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


class User(Base, table=True):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("email"),)

    firstname: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    email: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)
    avatar_id: Optional[int] = Field(foreign_key="attachment.id")
    disabled_at: Optional[datetime.datetime] = Field(sa_column=Column(DateTime(timezone=True)))

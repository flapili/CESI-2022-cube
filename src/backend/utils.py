# coding: utf-8
import hashlib
from pathlib import Path

import requests
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

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

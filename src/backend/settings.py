# coding: utf-8
from pathlib import Path
from functools import lru_cache

from pydantic import BaseSettings, SecretStr, Field


class Settings(BaseSettings):
    jwt_secret: SecretStr = Field(..., env="JWT_SECRET")

    postgres_host: str = Field("localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: SecretStr = Field(..., env="POSTGRES_PASSWORD")
    postgres_database: str = Field(..., env="POSTGRES_DATABASE")

    deployment_domain: str = Field(..., env="DEPLOYMENT_DOMAIN")

    mailjet_apikey_public: SecretStr = Field(..., env="MAILJET_APIKEY_PUBLIC")
    mailjet_apikey_private: SecretStr = Field(..., env="MAILJET_APIKEY_PRIVATE")
    mailjet_sender_email: str = Field(..., env="MAILJET_SENDER_EMAIL")
    mailjet_sender_name: str = Field(..., env="MAILJET_SENDER_NAME")

    class Config:
        env_file = Path(__file__).resolve().parent / ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

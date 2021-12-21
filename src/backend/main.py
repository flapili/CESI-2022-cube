# coding: utf-8
from pathlib import Path
from importlib import import_module

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import get_settings

settings = get_settings()
Path("attachments").mkdir(exist_ok=True)

app = FastAPI()
cors_origins = [settings.front_deployment_domain]
if settings.mode == "development":
    cors_origins.append("http://localhost:8000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for router in Path("routers").glob("**/*.py"):
    normalized_path = ".".join(router.parts[:-1] + (router.stem,))
    module = import_module(normalized_path)
    router_prefix = "/".join(router.parts[1:-1] + (router.stem,))
    app.include_router(module.router, prefix=f"/{router_prefix}", tags=[router.stem])

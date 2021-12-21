# coding: utf-8
from pathlib import Path
from importlib import import_module

from fastapi import FastAPI

Path("attachments").mkdir(exist_ok=True)

app = FastAPI()
for router in Path("routers").glob("**/*.py"):
    normalized_path = ".".join(router.parts[:-1] + (router.stem,))
    module = import_module(normalized_path)
    router_prefix = "/".join(router.parts[1:-1] + (router.stem,))
    app.include_router(module.router, prefix=f"/{router_prefix}", tags=[router.stem])

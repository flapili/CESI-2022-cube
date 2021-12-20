# coding: utf-8
from pathlib import Path
from importlib import import_module

from fastapi import FastAPI


app = FastAPI()


for file in Path("routes").glob("**/handler_*.py"):
    normalized_path = ".".join(file.parts[:-1] + (file.stem,))
    module = import_module(normalized_path)
    register_route_function = getattr(module, "register_route", None)
    if register_route_function is not None:
        register_route_function(app)
    else:
        print("[warning] {file} has not attribute 'register_route'")

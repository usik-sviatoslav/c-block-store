from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.django.asgi import app as django_app

from .urls import api_router

app = FastAPI()
app.include_router(api_router)

app.mount("/django", django_app)  # type: ignore
app.mount("/static", StaticFiles(directory="static"), name="static")

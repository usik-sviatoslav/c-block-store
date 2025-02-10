from fastapi import APIRouter

from .utils import health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", include_in_schema=False)

from fastapi import APIRouter

from api.routes import auth, health, user

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", include_in_schema=False)
api_router.include_router(auth.router, prefix="/auth", tags=["Authorization"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])

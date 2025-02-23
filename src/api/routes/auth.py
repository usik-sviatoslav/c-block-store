from asgiref.sync import sync_to_async
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv

from api.schemas.auth import LoginRequestForm, RefreshTokenRequestForm, RegisterRequestForm, TokenPair
from api.utils.jwt import create_token_pair, refresh_access_token
from apps.user.models import User
from core.fastapi.exceptions import (
    InvalidCredentialsException,
    InvalidEmailOrPasswordException,
    UserAlreadyExistsException,
)

router = APIRouter()


@cbv(router)
class AuthView:
    @router.post("/token/obtain")
    async def obtain_token_pair(self, form_data: OAuth2PasswordRequestForm = Depends()) -> TokenPair:
        user = await User.objects.filter(username=form_data.username).afirst()

        if not user or not await user.acheck_password(form_data.password):
            raise InvalidCredentialsException()

        return TokenPair(**create_token_pair(data={"sub": str(user.id)}))

    @router.post("/token/refresh")
    async def refresh_token(self, form_data: RefreshTokenRequestForm = Depends()) -> TokenPair:
        return TokenPair(**refresh_access_token(form_data.refresh_token))

    @router.post("/register")
    async def register_user(self, form_data: RegisterRequestForm = Depends()) -> TokenPair:
        if await User.objects.filter(email=form_data.email).afirst():
            raise UserAlreadyExistsException()

        user = await sync_to_async(User.objects.create_user)(**form_data.__dict__)
        return TokenPair(**create_token_pair(data={"sub": str(user.id)}))

    @router.post("/login")
    async def login(self, form_data: LoginRequestForm = Depends()) -> TokenPair:
        user = await User.objects.filter(email=form_data.email).afirst()

        if not user or not await user.acheck_password(form_data.password):
            raise InvalidEmailOrPasswordException()

        return TokenPair(**create_token_pair(data={"sub": str(user.id)}))

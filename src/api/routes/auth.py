from asgiref.sync import sync_to_async
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv

from api.crud.auth import CRUDAuth
from api.schemas.auth import LoginRequestForm, RefreshTokenRequestForm, RegisterRequestForm, TokenPair
from api.utils.jwt import create_token_pair, refresh_access_token

router = APIRouter()


@cbv(router)
class AuthView(CRUDAuth):
    @router.post("/token/obtain")
    async def obtain_token_pair(self, form_data: OAuth2PasswordRequestForm = Depends()) -> TokenPair:
        return await self.obtain(username=form_data.username, password=form_data.password)

    @router.post("/token/refresh")
    async def refresh_token(self, form_data: RefreshTokenRequestForm = Depends()) -> TokenPair:
        return refresh_access_token(form_data.refresh_token)

    @router.post("/register")
    async def register_user(self, form_data: RegisterRequestForm = Depends()) -> TokenPair:
        await self.validate_user(email=form_data.email, password=form_data.password, raise_if_exists=True)
        user = await sync_to_async(self.model.objects.create_user)(**form_data.model_dump())
        return create_token_pair(data={"sub": str(user.id)})

    @router.post("/login")
    async def login(self, form_data: LoginRequestForm = Depends()) -> TokenPair:
        return await self.obtain(email=form_data.email, password=form_data.password)

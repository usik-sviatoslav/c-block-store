from fastapi import Form
from pydantic import BaseModel, EmailStr

from api.schemas.user import UserCreateSchema


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequestForm:
    def __init__(self, refresh_token: str = Form(...)):
        self.refresh_token = refresh_token


class RegisterRequestForm(UserCreateSchema):
    def __init__(
        self,
        email: EmailStr = Form(...),
        password: str = Form(...),
        username: str | None = Form(None),
        first_name: str | None = Form(None),
        last_name: str | None = Form(None),
    ):
        super().__init__(
            email=email,
            password=password,
            username=username if username else str(email).split("@")[0],
            first_name=first_name,
            last_name=last_name,
        )


class LoginRequestForm:
    def __init__(
        self,
        email: EmailStr = Form(...),
        password: str = Form(...),
    ):
        self.email = email
        self.password = password

from typing import Optional

from fastapi import Form
from pydantic import BaseModel, EmailStr


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequestForm:
    def __init__(self, refresh_token: str = Form(...)):
        self.refresh_token = refresh_token


class RegisterRequestForm:
    def __init__(
        self,
        email: EmailStr = Form(...),
        password: str = Form(...),
        username: Optional[str] = Form(None),
        first_name: Optional[str] = Form(None),
        last_name: Optional[str] = Form(None),
    ):
        self.email = email
        self.password = password
        self.username = username if username else str(email).split("@")[0]
        self.first_name = first_name
        self.last_name = last_name


class LoginRequestForm:
    def __init__(
        self,
        email: EmailStr = Form(...),
        password: str = Form(...),
    ):
        self.email = email
        self.password = password

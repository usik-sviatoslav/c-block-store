from pydantic import EmailStr

from .base import BaseModelSchema


class UserReadSchema(BaseModelSchema):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    is_verified: bool


class UserCreateSchema(BaseModelSchema):
    email: EmailStr
    password: str
    username: str | None
    first_name: str | None
    last_name: str | None

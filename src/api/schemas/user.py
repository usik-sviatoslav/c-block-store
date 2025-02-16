from pydantic import EmailStr

from .base import BaseModelSchema


class UserReadSchema(BaseModelSchema):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    is_verified: bool

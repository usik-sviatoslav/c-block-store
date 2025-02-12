from pydantic import BaseModel, EmailStr


class UserRetrieve(BaseModel):
    class Config:
        from_attributes = True

    email: EmailStr
    username: str
    first_name: str
    last_name: str
    is_verified: bool

from datetime import datetime, timedelta, timezone
from typing import Any, Literal, TypedDict

import jwt
from fastapi.security import OAuth2PasswordBearer
from pydantic.v1 import BaseSettings

from api.schemas.auth import TokenPair
from core.fastapi.exceptions import ExpiredTokenException, InvalidTokenException

__all__ = [
    "oauth2_scheme",
    "verify_token",
    "create_token_pair",
    "refresh_access_token",
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token/obtain")


class TokenSecrets(TypedDict):
    access: str
    refresh: str


class TokenExpire(TypedDict):
    access: timedelta
    refresh: timedelta


class TokenSettings(BaseSettings):
    TOKEN_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_SECRET_KEY: str = "secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_TOKEN_SECRET_KEY: str = "refresh_secret_key"
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def secret_key(self) -> TokenSecrets:
        return TokenSecrets(
            access=self.ACCESS_TOKEN_SECRET_KEY,
            refresh=self.REFRESH_TOKEN_SECRET_KEY,
        )

    @property
    def expirations(self) -> TokenExpire:
        return TokenExpire(
            access=timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
            refresh=timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS),
        )


jwt_token = TokenSettings()


def create_token(data: dict, token_type: Literal["access", "refresh"]) -> str:
    payload = {**data, "exp": datetime.now(timezone.utc) + jwt_token.expirations[token_type]}
    return jwt.encode(payload, jwt_token.secret_key[token_type], algorithm=jwt_token.TOKEN_ALGORITHM)


def verify_token(token: str, token_type: Literal["access", "refresh"]) -> Any:
    try:
        return jwt.decode(token, jwt_token.secret_key[token_type], algorithms=[jwt_token.TOKEN_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except jwt.PyJWTError:
        raise InvalidTokenException()


def create_token_pair(data: dict) -> TokenPair:
    return TokenPair(
        access_token=create_token(data, "access"),
        refresh_token=create_token(data, "refresh"),
        token_type="bearer",
    )


def refresh_access_token(refresh_token: str) -> TokenPair:
    payload = verify_token(refresh_token, "refresh")

    if "sub" not in payload:
        raise InvalidTokenException()

    return TokenPair(
        access_token=create_token({"sub": payload["sub"]}, "access"),
        refresh_token=refresh_token,
        token_type="bearer",
    )

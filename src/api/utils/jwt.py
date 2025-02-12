import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Literal

import jwt
from fastapi.security import OAuth2PasswordBearer

from core.fastapi.exceptions import ExpiredTokenException, InvalidTokenException

__all__ = [
    "oauth2_scheme",
    "verify_token",
    "create_token_pair",
    "refresh_access_token",
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token/obtain")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 30


SECRET_KEYS = {
    "access": os.getenv("SECRET_KEY", "secret_key"),
    "refresh": os.getenv("REFRESH_SECRET_KEY", "refresh_secret_key"),
}
EXPIRATION_TIMES = {
    "access": timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    "refresh": timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
}


def create_token(data: dict, token_type: Literal["access", "refresh"]) -> str:
    payload = {**data, "exp": datetime.now(timezone.utc) + EXPIRATION_TIMES[token_type]}
    return jwt.encode(payload, SECRET_KEYS[token_type], algorithm=ALGORITHM)


def verify_token(token: str, token_type: Literal["access", "refresh"]) -> Any:
    try:
        return jwt.decode(token, SECRET_KEYS[token_type], algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except jwt.PyJWTError:
        raise InvalidTokenException()


def create_token_pair(data: dict) -> Dict[str, str]:
    return {
        "access_token": create_token(data, "access"),
        "refresh_token": create_token(data, "refresh"),
        "token_type": "bearer",
    }


def refresh_access_token(refresh_token: str) -> Dict[str, str]:
    payload = verify_token(refresh_token, "refresh")

    if "sub" not in payload:
        raise InvalidTokenException()

    return {
        "access_token": create_token({"sub": payload["sub"]}, "access"),
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

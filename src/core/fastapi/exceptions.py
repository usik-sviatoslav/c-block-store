from fastapi import HTTPException, status


class ExpiredTokenException(HTTPException):
    def __init__(self) -> None:
        self.status_code: int = status.HTTP_401_UNAUTHORIZED
        self.detail: str = "Token has expired."
        super().__init__(self.status_code, self.detail)


class InvalidTokenException(HTTPException):
    def __init__(self) -> None:
        self.status_code: int = status.HTTP_401_UNAUTHORIZED
        self.detail: str = "Invalid token."
        super().__init__(self.status_code, self.detail)


class InvalidEmailOrPasswordException(HTTPException):
    def __init__(self) -> None:
        self.status_code: int = status.HTTP_400_BAD_REQUEST
        self.detail: str = "Invalid email or password."
        super().__init__(self.status_code, self.detail)


class InvalidCredentialsException(HTTPException):
    def __init__(self) -> None:
        self.status_code: int = status.HTTP_400_BAD_REQUEST
        self.detail: str = "Invalid credentials."
        super().__init__(self.status_code, self.detail)


class UserAlreadyExistsException(HTTPException):
    def __init__(self) -> None:
        self.status_code: int = status.HTTP_400_BAD_REQUEST
        self.detail: str = "User already exists."
        super().__init__(self.status_code, self.detail)


class BlockNotFoundException(HTTPException):
    def __init__(self) -> None:
        self.status_code: int = status.HTTP_404_NOT_FOUND
        self.detail: str = "No Block matches the given query."
        super().__init__(self.status_code, self.detail)


class ProviderNotFoundException(HTTPException):
    def __init__(self) -> None:
        self.status_code: int = status.HTTP_404_NOT_FOUND
        self.detail: str = "No Provider matches the given query."
        super().__init__(self.status_code, self.detail)

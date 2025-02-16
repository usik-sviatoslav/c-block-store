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


class ObjectNotFoundException(HTTPException):
    def __init__(self, model_name: str, plural: bool = False) -> None:
        self.status_code: int = status.HTTP_404_NOT_FOUND
        self.detail: str = f"No {model_name}{'s' if plural else ''} matches the given query."
        super().__init__(self.status_code, self.detail)


class ObjectAlreadyExistsException(HTTPException):
    def __init__(self, model_name: str) -> None:
        self.status_code: int = status.HTTP_400_BAD_REQUEST
        self.detail: str = f"{model_name} already exists."
        super().__init__(self.status_code, self.detail)

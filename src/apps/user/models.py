from typing import Any, ClassVar

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.django.db.models import UUIDv7Model

from .validators import validate_email, validate_name, validate_username


class CustomUserManager(UserManager["User"]):
    def create_superuser(
        self, username: str, email: str | None = None, password: str | None = None, **extra_fields: Any
    ) -> "User":
        extra_fields.setdefault("is_verified", True)
        return super().create_superuser(username, email, password, **extra_fields)


class User(UUIDv7Model, AbstractUser):
    class Meta:
        db_table = "user"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(_("email"), unique=True, validators=[validate_email])
    username = models.CharField(_("username"), max_length=150, validators=[validate_username])

    first_name = models.CharField(_("first name"), max_length=150, blank=True, validators=[validate_name])
    last_name = models.CharField(_("last name"), max_length=150, blank=True, validators=[validate_name])

    is_verified = models.BooleanField(_("verified"), default=False)

    objects: ClassVar[CustomUserManager] = CustomUserManager()

    def __str__(self) -> str:
        return self.username

    def verify(self) -> None:
        self.is_verified = True
        self.save(force_update=True, update_fields=["is_verified"])

    def set_new_password(self, raw_password: str) -> None:
        super().set_password(raw_password)
        self.save(force_update=True, update_fields=["password"])

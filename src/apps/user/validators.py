from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator, RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

__all__ = [
    "validate_name",
    "validate_email",
    "validate_username",
]


@deconstructible
class NameValidator(RegexValidator):
    regex = r"^[A-Za-zА-Яа-яІіЄєЇї]+$"
    message = _("Enter a valid name containing only letters.")
    flags = 0


validate_name = NameValidator()
validate_email = EmailValidator()
validate_username = UnicodeUsernameValidator()

from django.core.validators import RegexValidator


def github_url_validator(value: str) -> None:
    """
    Checking that the string startswith github.com and user after slash.
    """
    reg_validator = RegexValidator(
        regex=r'^https://github.com/.*/',
        message='Введите корректный URL GitHub репозитория'
    )
    reg_validator(value)

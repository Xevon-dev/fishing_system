

from accounts.session import current_user

__all__ = ("current_user", "as_int")


def as_int(value):
    return int(value) if value and value.isdigit() else None

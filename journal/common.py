from accounts.session import current_user


def as_int(value):
    return int(value) if value and value.isdigit() else None

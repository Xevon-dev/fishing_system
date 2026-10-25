from .session import current_user as get_current_user


def current_user(request):
    return {"current_user": get_current_user(request)}

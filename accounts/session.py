from .models import Users

def current_user(request):
    if hasattr(request, "_fishwise_current_user"):
        return request._fishwise_current_user

    user_id = request.session.get("user_id")
    if not user_id:
        request._fishwise_current_user = None
        return None

    user = Users.objects.select_related("level").filter(pk=user_id).first()
    if not user:
        request.session.pop("user_id", None)

    request._fishwise_current_user = user
    return user


def login_user(request, user):
    request.session["user_id"] = user.user_id
    request._fishwise_current_user = user


def logout_user(request):
    request.session.pop("user_id", None)
    request._fishwise_current_user = None

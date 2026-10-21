from .models import Users

def current_user(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None

    user = Users.objects.select_related("level").filter(pk=user_id).first()
    if not user:
        request.session.pop("user_id", None)

    return user


def login_user(request, user):
    request.session["user_id"] = user.user_id


def logout_user(request):
    request.session.pop("user_id", None)

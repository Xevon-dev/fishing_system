from .models import Users


def current_user(request):
    user_id = request.session.get("user_id")
    user = None
    if user_id:
        try:
            user = Users.objects.select_related("level").get(pk=user_id)
        except Users.DoesNotExist:
            user = None
    return {"current_user": user}
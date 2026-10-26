

from django.shortcuts import redirect, render

from ..session import current_user
from ..validators import username_error


def username_view(request):
    user = current_user(request)
    if not user:
        return redirect("accounts:login")

    errors = {}
    username = user.username

    if request.method == "POST":
        username = request.POST.get("username", "").strip()

        message = username_error(username, exclude_user_id=user.user_id)
        if message:
            errors["username"] = message

        if not errors:
            user.username = username
            user.save(update_fields=["username"])
            return redirect("accounts:profile")

    return render(request, "username.html", {
        "errors": errors,
        "username": username,
    })

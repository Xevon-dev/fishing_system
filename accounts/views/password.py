

from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect, render

from ..session import current_user
from ..validators import password_strength_error


def password_view(request):
    user = current_user(request)
    if not user:
        return redirect("accounts:login")

    errors = {}
    fields = {
        "current_password": "",
        "new_password": "",
        "confirm_password": "",
    }

    if request.method == "POST":
        fields = {
            "current_password": request.POST.get("current_password", ""),
            "new_password": request.POST.get("new_password", ""),
            "confirm_password": request.POST.get("confirm_password", ""),
        }

        if not fields["current_password"]:
            errors["current_password"] = "Введіть поточний пароль"
        elif not check_password(fields["current_password"], user.password_hash):
            errors["current_password"] = "Невірний поточний пароль"

        message = password_strength_error(
            fields["new_password"], username=user.username, email=user.email
        )
        if message:
            errors["new_password"] = message
        elif check_password(fields["new_password"], user.password_hash):
            errors["new_password"] = "Новий пароль такий самий, як старий"

        if not fields["confirm_password"]:
            errors["confirm_password"] = "Підтвердіть новий пароль"
        elif fields["confirm_password"] != fields["new_password"]:
            errors["confirm_password"] = "Паролі не збігаються"

        if not errors:
            user.password_hash = make_password(fields["new_password"])
            user.save(update_fields=["password_hash"])
            return redirect("accounts:profile")

        if request.POST.get("return_to_profile") == "1":
            request.session["profile_password_errors"] = errors
            return redirect("accounts:profile")

    return render(request, "password.html", {
        "errors": errors,
        "fields": fields,
    })



from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect, render

from ..session import current_user


def password_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

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

        if not fields["new_password"]:
            errors["new_password"] = "Введіть новий пароль"
        elif len(fields["new_password"]) < 6:
            errors["new_password"] = "Мінімум 6 символів"
        elif fields["new_password"] == fields["current_password"]:
            errors["new_password"] = "Новий пароль такий самий, як старий"

        if not fields["confirm_password"]:
            errors["confirm_password"] = "Підтвердіть новий пароль"
        elif fields["confirm_password"] != fields["new_password"]:
            errors["confirm_password"] = "Паролі не збігаються"

        if not errors:
            user.password_hash = make_password(fields["new_password"])
            user.save(update_fields=["password_hash"])
            return redirect("profile")

    return render(request, "password.html", {
        "errors": errors,
        "fields": fields,
    })

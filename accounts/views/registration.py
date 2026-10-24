from urllib.parse import quote

from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache

from ..levels import LEVEL_NAMES
from ..models import Levels, Users
from ..validators import email_error, password_errors, username_error


@never_cache
def register_view(request):
    errors = {}
    form = {
        "username": "",
        "email": "",
        "fishing_level": request.GET.get("fishing_level", ""),
    }

    if request.method == "POST":
        form["username"] = request.POST.get("username", "").strip()
        form["email"] = request.POST.get("email", "").strip()
        form["fishing_level"] = request.POST.get("fishing_level", "")
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        for field, message in (
            ("username", username_error(form["username"])),
            ("email", email_error(form["email"])),
        ):
            if message:
                errors[field] = message

        errors.update(password_errors(password, confirm_password))

        if form["fishing_level"] not in LEVEL_NAMES:
            errors["fishing_level"] = "Оберіть рівень риболовлі"

        if not errors:
            level, _ = Levels.objects.get_or_create(
                name=LEVEL_NAMES[form["fishing_level"]],
            )
            Users.objects.create(
                username=form["username"],
                email=form["email"],
                password_hash=make_password(password),
                level=level,
                created_at=timezone.now(),
            )
            return redirect(f"{reverse('login')}?login={quote(form['username'])}")

    return render(request, "register.html", {
        "errors": errors,
        "username": form["username"],
        "email": form["email"],
        "fishing_level": form["fishing_level"],
    })

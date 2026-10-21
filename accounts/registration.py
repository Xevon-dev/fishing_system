import re

from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from django.utils import timezone

from .levels import LEVEL_NAMES
from .models import Levels, Users
from .session import login_user

EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
USERNAME_RE = re.compile(r"[\w]+")

def username_error(username):
    if not username:
        return "Введіть ім'я користувача"
    if len(username) < 3:
        return "Мінімум 3 символи"
    if len(username) > 150:
        return "Ім'я занадто довге"
    if not USERNAME_RE.fullmatch(username):
        return "Використовуйте літери, цифри або _"
    return None


def email_error(email):
    if not email:
        return "Введіть електронну пошту"
    if not EMAIL_RE.fullmatch(email):
        return "Некоректна електронна пошта"
    if Users.objects.filter(email=email).exists():
        return "Така пошта вже зареєстрована"
    return None


def password_errors(password, confirm_password):
    errors = {}

    if not password:
        errors["password"] = "Введіть пароль"
    elif len(password) < 6:
        errors["password"] = "Мінімум 6 символів"

    if not confirm_password:
        errors["confirm_password"] = "Підтвердіть пароль"
    elif password != confirm_password:
        errors["confirm_password"] = "Паролі не збігаються"

    return errors


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
            user = Users.objects.create(
                username=form["username"],
                email=form["email"],
                password_hash=make_password(password),
                level=level,
                created_at=timezone.now(),
            )
            login_user(request, user)
            return redirect("profile")

    return render(request, "register.html", {
        "errors": errors,
        "username": form["username"],
        "email": form["email"],
        "fishing_level": form["fishing_level"],
    })

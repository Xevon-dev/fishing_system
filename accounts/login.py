"""Вхід і вихід із системи."""

import re

from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render

from .models import Users
from .session import login_user, logout_user

EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def login_view(request):
    errors = {}
    email = ""

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not email:
            errors["email"] = "Введіть email"
        elif not EMAIL_RE.fullmatch(email):
            errors["email"] = "Некоректна електронна пошта"

        if not password:
            errors["password"] = "Введіть пароль"

        if not errors:
            user = Users.objects.filter(email=email).first()

            if not user:
                errors["email"] = "Користувача з такою поштою немає"
            elif not check_password(password, user.password_hash):
                errors["password"] = "Невірний пароль"
            else:
                login_user(request, user)
                return redirect("profile")

    return render(request, "login.html", {"errors": errors, "email": email})


def logout_view(request):
    logout_user(request)
    return redirect("home")

import re

from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from ..models import Users
from ..session import login_user, logout_user

EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


@never_cache
def login_view(request):
    errors = {}
    login_value = request.GET.get("login", "").strip()

    if request.method == "POST":
        login_value = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not login_value:
            errors["username"] = "Введіть логін"
        elif "@" in login_value and not EMAIL_RE.fullmatch(login_value):
            errors["username"] = "Некоректна електронна пошта"

        if not password:
            errors["password"] = "Введіть пароль"

        if not errors:
            user = Users.objects.filter(username=login_value).first()

            if not user and "@" in login_value:
                user = Users.objects.filter(email=login_value).first()

            if not user:
                errors["username"] = "Користувача з таким логіном немає"
            elif not check_password(password, user.password_hash):
                errors["password"] = "Невірний пароль"
            else:
                login_user(request, user)
                return redirect("profile")

    return render(request, "login.html", {"errors": errors, "login": login_value})


@require_POST
def logout_view(request):
    logout_user(request)
    return redirect("home")

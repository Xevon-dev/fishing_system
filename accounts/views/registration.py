from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth.hashers import is_password_usable
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache

from ..forms import RegistrationForm
from ..models import Users


@never_cache
def register_view(request):
    if request.session.pop("google_registration_required", False):
        messages.warning(request, "Щоб увійти через Google, спершу зареєструйтеся на сайті.")

    google_user_id = request.session.get("google_registration_user_id")
    existing_google_user = Users.objects.filter(user_id=google_user_id).first() if google_user_id else None
    if existing_google_user and is_password_usable(existing_google_user.password_hash):
        existing_google_user = None
        request.session.pop("google_registration_user_id", None)

    initial_level = request.GET.get("fishing_level", "")
    form = RegistrationForm(
        request.POST or None,
        initial={
            "fishing_level": initial_level,
            "username": existing_google_user.username if existing_google_user else "",
            "email": existing_google_user.email if existing_google_user else "",
        },
        existing_google_user=existing_google_user,
    )
    if request.method == "POST" and form.is_valid():
        user = form.save()
        request.session.pop("google_registration_user_id", None)
        return redirect(f"{reverse('accounts:login')}?login={quote(user.username)}")

    errors = {
        "username": form["username"].errors[0] if form["username"].errors else "",
        "email": form["email"].errors[0] if form["email"].errors else "",
        "password": form["password1"].errors[0] if form["password1"].errors else "",
        "confirm_password": form["password2"].errors[0] if form["password2"].errors else "",
        "fishing_level": form["fishing_level"].errors[0] if form["fishing_level"].errors else "",
    }
    return render(request, "register.html", {
        "errors": errors,
        "username": form["username"].value() or "",
        "email": form["email"].value() or "",
        "fishing_level": form["fishing_level"].value() or initial_level,
    })

from urllib.parse import quote

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache

from ..forms import RegistrationForm


@never_cache
def register_view(request):
    initial_level = request.GET.get("fishing_level", "")
    form = RegistrationForm(
        request.POST or None,
        initial={"fishing_level": initial_level},
    )
    if request.method == "POST" and form.is_valid():
        user = form.save()
        return redirect(f"{reverse('login')}?login={quote(user.username)}")

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

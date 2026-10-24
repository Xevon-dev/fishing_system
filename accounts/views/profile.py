from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Max, Sum
from django.shortcuts import redirect, render

from journal.models import Catches, FishingTrips, Tips
from ..models import Users
from ..session import current_user
from ..validators import email_error, username_error


def is_expert(user):
    return bool(user.level and user.level.name == "Досвідчений")


def format_weight(value):
    if not value:
        return "0"

    return f"{value:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def profile_context(user):
    tips = []
    if is_expert(user):
        tips = (
            Tips.objects
            .filter(author_id=user.user_id)
            .select_related("fish")
            .order_by("-tip_id")[:10]
        )

    trips = FishingTrips.objects.filter(user_id=user.user_id)
    catches = Catches.objects.filter(trip__user_id=user.user_id)
    weighed = catches.filter(weight_kg__isnull=False)

    return {
        "profile_user": user,
        "is_expert": is_expert(user),
        "trips": (
            trips
            .select_related("water_body", "type", "method")
            .prefetch_related("catches_set__fish")
            .order_by("-created_at")[:10]
        ),
        "tip_count": len(tips),
        "tips": tips,
        "trip_count": trips.count(),
        "total_weight": format_weight(weighed.aggregate(Sum("weight_kg"))["weight_kg__sum"]),
        "max_weight": format_weight(weighed.aggregate(Max("weight_kg"))["weight_kg__max"]),
    }


def profile_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

    return render(request, "profile.html", profile_context(user))


def edit_errors_for(user, form):
    errors = {}

    message = username_error(form["username"])
    if message:
        errors["username"] = message

    if form["email"] != user.email:
        message = email_error(form["email"])
        if message:
            errors["email"] = message

    password_fields = (
        form["current_password"] or
        form["new_password"] or
        form["confirm_password"]
    )
    if password_fields:
        if not form["current_password"]:
            errors["current_password"] = "Введіть поточний пароль"
        elif not check_password(form["current_password"], user.password_hash):
            errors["current_password"] = "Невірний поточний пароль"

        if not form["new_password"]:
            errors["new_password"] = "Введіть новий пароль"
        elif len(form["new_password"]) < 6:
            errors["new_password"] = "Мінімум 6 символів"
        elif form["new_password"] == form["current_password"]:
            errors["new_password"] = "Новий пароль має відрізнятися від поточного"

        if not form["confirm_password"]:
            errors["confirm_password"] = "Підтвердіть новий пароль"
        elif form["confirm_password"] != form["new_password"]:
            errors["confirm_password"] = "Паролі не збігаються"

    return errors


def profile_edit_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

    form = {
        "username": user.username,
        "email": user.email,
        "current_password": "",
        "new_password": "",
        "confirm_password": "",
    }

    if request.method != "POST":
        return redirect("profile")

    for field in form:
        form[field] = request.POST.get(field, "")

    form["username"] = form["username"].strip()
    form["email"] = form["email"].strip()

    errors = edit_errors_for(user, form)

    if errors:
        context = profile_context(user)
        context.update({
            "edit_form": form,
            "edit_errors": errors,
        })
        return render(request, "profile.html", context)

    fields = ["username"]
    user.username = form["username"]

    if form["email"] != user.email:
        user.email = form["email"]
        fields.append("email")

    if form["new_password"]:
        user.password_hash = make_password(form["new_password"])
        fields.append("password_hash")

    user.save(update_fields=fields)

    return redirect("profile")

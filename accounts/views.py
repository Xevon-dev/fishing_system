import json
import re

from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Levels, Users


LEVEL_NAME_MAP = {
    "beginner": "Початківець",
    "intermediate": "Середній",
    "advanced": "Досвідчений",
}



QUESTIONS_FILE = "accounts/data/questions.json"



def fishing_test_view(request):
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)["questions"]

    public_questions = []

    for question in questions:
        answers = []

        for answer in question["answers"]:
            answers.append({
                "id": answer["id"],
                "text": answer["text"]
            })

        public_questions.append({
            "id": question["id"],
            "question": question["question"],
            "answers": answers
        })

    if request.method == "POST":
        score = 0

        for question in questions:
            selected = request.POST.get(f"q{question['id']}")

            if not selected:
                return render(request, "fishing_test.html", {
                    "questions": public_questions,
                    "error": "Дайте відповідь на всі запитання.",
                    "completed": False
                })

            found = False

            for answer in question["answers"]:
                if str(answer["id"]) == selected:
                    score += answer["points"]
                    found = True
                    break

            if not found:
                return render(request, "fishing_test.html", {
                    "questions": public_questions,
                    "error": "Некоректна відповідь.",
                    "completed": False
                })

        if score <= 7:
            level = "beginner"
            level_name = "Початківець"
        elif score <= 12:
            level = "intermediate"
            level_name = "Середній"
        else:
            level = "advanced"
            level_name = "Досвідчений"

        return render(request, "fishing_test.html", {
            "completed": True,
            "level": level,
            "level_name": level_name
        })

    return render(request, "fishing_test.html", {
        "questions": public_questions,
        "completed": False
    })




def register_view(request):
    errors = {}
    username = ""
    email = ""

    fishing_level = request.GET.get("fishing_level", "")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        fishing_level = request.POST.get("fishing_level", "")

        if not username:
            errors["username"] = "Введіть ім'я користувача"
        elif len(username) < 3:
            errors["username"] = "Мінімум 3 символи"
        elif len(username) > 150:
            errors["username"] = "Ім'я занадто довге"
        elif not re.fullmatch(r"[\w]+", username):
            errors["username"] = "Використовуйте літери, цифри або _"

        if not email:
            errors["email"] = "Введіть електронну пошту"
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            errors["email"] = "Некоректна електронна пошта"
        elif Users.objects.filter(email=email).exists():
            errors["email"] = "Така пошта вже зареєстрована"

        if not password:
            errors["password"] = "Введіть пароль"
        elif len(password) < 6:
            errors["password"] = "Мінімум 6 символів"

        if not confirm_password:
            errors["confirm_password"] = "Підтвердіть пароль"
        elif password != confirm_password:
            errors["confirm_password"] = "Паролі не збігаються"

        if fishing_level not in ("beginner", "intermediate", "advanced"):
            errors["fishing_level"] = "Оберіть рівень риболовлі"

        if not errors:
            level_name = LEVEL_NAME_MAP[fishing_level]
            level_obj, _ = Levels.objects.get_or_create(name=level_name)

            user = Users.objects.create(
                username=username,
                email=email,
                password_hash=make_password(password),
                level=level_obj,
                created_at=timezone.now(),
            )

            request.session["user_id"] = user.user_id
            return redirect("profile")

    return render(request, "register.html", {
        "errors": errors,
        "username": username,
        "email": email,
        "fishing_level": fishing_level
    })



def login_view(request):
    errors = {}
    email = ""

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not email:
            errors["email"] = "Введіть email"
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            errors["email"] = "Некоректна електронна пошта"

        if not password:
            errors["password"] = "Введіть пароль"

        if not errors:
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                errors["email"] = "Користувача з такою поштою немає"
            else:
                if not check_password(password, user.password_hash):
                    errors["password"] = "Невірний пароль"
                else:
                    request.session["user_id"] = user.user_id
                    return redirect("profile")

    return render(request, "login.html", {
        "errors": errors,
        "email": email
    })


def profile_view(request):
    from journal.models import Catches, FishingTrips, Tips

    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    try:
        user = Users.objects.select_related("level").get(pk=user_id)
    except Users.DoesNotExist:
        request.session.pop("user_id", None)
        return redirect("login")

    trips = (
        FishingTrips.objects
        .filter(user_id=user.user_id)
        .select_related("water_body")
        .order_by("-start_time")[:10]
    )
    catches = (
        Catches.objects
        .filter(trip__user_id=user.user_id)
        .select_related("fish", "trip")
        .order_by("-catch_id")[:10]
    )
    tips = (
        Tips.objects
        .filter(author_id=user.user_id)
        .select_related("fish")
        .order_by("-tip_id")[:10]
    )

    return render(request, "profile.html", {
        "profile_user": user,
        "trips": trips,
        "catches": catches,
        "tips": tips,
    })


def logout_view(request):
    request.session.pop("user_id", None)
    return redirect("home")

import json
import re

from django.shortcuts import render, redirect



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
            return redirect("login")

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
            return redirect("home")

    return render(request, "login.html", {
        "errors": errors,
        "email": email
    })

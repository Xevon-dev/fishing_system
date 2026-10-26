from django.shortcuts import redirect, render

from ..levels import LEVEL_NAMES, level_from_score
from ..questions import load_questions, public_questions
from ..session import current_user
from ..models import Levels, Users
from django.db import transaction


def count_score(questions, post):
    score = 0

    for question in questions:
        selected = post.get(f"q{question['id']}")

        if not selected:
            return None, "Дайте відповідь на всі запитання."

        points = next(
            (
                answer["points"]
                for answer in question["answers"]
                if str(answer["id"]) == selected
            ),
            None,
        )

        if points is None:
            return None, "Некоректна відповідь."

        score += points

    return score, None


def fishing_test_view(request):
    questions = load_questions()
    user = current_user(request)
    context = {
        "questions": public_questions(questions),
        "completed": False,
    }

    if request.method == "POST" and request.POST.get("action") == "cancel_level_change":
        request.session.pop("pending_fishing_level", None)
        return redirect("accounts:profile" if user else "accounts:register")

    if request.method == "POST" and request.POST.get("action") == "confirm_level_change":
        pending_level = request.session.pop("pending_fishing_level", None)
        if not user:
            return redirect("accounts:register")
        if pending_level not in LEVEL_NAMES:
            return redirect("accounts:fishing_test")
        with transaction.atomic():
            user = Users.objects.select_for_update().select_related("level").get(pk=user.pk)
            can_upgrade = user.level and user.level.name in {"Початківець", "Середній"}
            if can_upgrade and user.level.name != LEVEL_NAMES[pending_level]:
                user.level, _ = Levels.objects.get_or_create(name=LEVEL_NAMES[pending_level])
                user.save(update_fields=["level"])
        return __import__("django.shortcuts", fromlist=["redirect"]).redirect("accounts:profile")

    if request.method != "POST":
        return render(request, "fishing_test.html", context)

    score, error = count_score(questions, request.POST) if questions else (None, "Запитання тесту ще не додані.")

    if error:
        context["error"] = error
        return render(request, "fishing_test.html", context)

    level = level_from_score(score, len(questions))
    if user:
        user = Users.objects.select_related("level").get(pk=user.pk)
        can_confirm_level = bool(user.level and user.level.name in {"Початківець", "Середній"})
        request.session["pending_fishing_level"] = level
        context["saved_level"] = user.level.name if user.level else "Не обрано"
        context["can_confirm_level"] = can_confirm_level
        context["current_user"] = user
    context.update({
        "completed": True,
        "level": level,
        "level_name": LEVEL_NAMES[level],
    })
    return render(request, "fishing_test.html", context)

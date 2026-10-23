from django.shortcuts import render

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

    if request.method != "POST":
        return render(request, "fishing_test.html", context)

    score, error = count_score(questions, request.POST) if questions else (None, "Запитання тесту ще не додані.")

    if error:
        context["error"] = error
        return render(request, "fishing_test.html", context)

    level = level_from_score(score, len(questions))
    if user:
        with transaction.atomic():
            user = Users.objects.select_for_update().select_related("level").get(pk=user.pk)
            ranks = list(LEVEL_NAMES.values())
            current_rank = ranks.index(user.level.name) if user.level and user.level.name in ranks else -1
            if ranks.index(LEVEL_NAMES[level]) > current_rank:
                user.level, _ = Levels.objects.get_or_create(name=LEVEL_NAMES[level])
                user.save(update_fields=["level"])
                context["upgraded"] = True
            context["saved_level"] = user.level.name if user.level else "Не обрано"
            context["current_user"] = user
    context.update({
        "completed": True,
        "level": level,
        "level_name": LEVEL_NAMES[level],
    })
    return render(request, "fishing_test.html", context)

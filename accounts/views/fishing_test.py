from django.shortcuts import render

from ..levels import LEVEL_NAMES, level_from_score
from ..questions import load_questions, public_questions


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
    context = {
        "questions": public_questions(questions),
        "completed": False,
    }

    if request.method != "POST":
        return render(request, "fishing_test.html", context)

    score, error = count_score(questions, request.POST)

    if error:
        context["error"] = error
        return render(request, "fishing_test.html", context)

    level = level_from_score(score)
    context.update({
        "completed": True,
        "level": level,
        "level_name": LEVEL_NAMES[level],
    })
    return render(request, "fishing_test.html", context)

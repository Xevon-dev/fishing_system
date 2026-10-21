"""Запитання тесту на рівень рибалки."""

import json
from pathlib import Path

from django.conf import settings

QUESTIONS_FILE = Path(settings.BASE_DIR) / "accounts" / "data" / "questions.json"


def load_questions():
    with open(QUESTIONS_FILE, encoding="utf-8") as file:
        return json.load(file)["questions"]


def public_questions(questions):
    """Ті самі питання, але без правильних балів — для шаблону."""
    return [
        {
            "id": question["id"],
            "question": question["question"],
            "answers": [
                {"id": answer["id"], "text": answer["text"]}
                for answer in question["answers"]
            ],
        }
        for question in questions
    ]

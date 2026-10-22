from .models import TestQuestions


def load_questions():
    return [
        {
            "id": question.question_id,
            "question": question.text,
            "answers": [
                {
                    "id": answer.answer_id,
                    "text": answer.text,
                    "points": answer.points,
                }
                for answer in question.answers.all()
            ],
        }
        for question in TestQuestions.objects.prefetch_related("answers")
    ]


def public_questions(questions):
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

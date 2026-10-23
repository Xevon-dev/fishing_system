from django.db import migrations


QUESTIONS = [
    ("Як ви підбираєте снасті під умови водойми?", [
        ("Користуюся одним комплектом і ще вчуся", 1),
        ("Обираю снасті за порадою знайомих", 2),
        ("Враховую вид риби, глибину та течію", 3),
        ("Самостійно налаштовую оснащення й змінюю його під умови", 4),
    ]),
    ("Що ви робите, якщо риба не клює?", [
        ("Просто чекаю або завершую риболовлю", 1),
        ("Пробую іншу наживку", 2),
        ("Змінюю місце, глибину або спосіб подачі приманки", 3),
        ("Послідовно перевіряю умови та оснащення, аналізую результат", 4),
    ]),
]


def add_questions(apps, schema_editor):
    Question = apps.get_model("accounts", "TestQuestions")
    Answer = apps.get_model("accounts", "TestAnswers")
    last = Question.objects.order_by("-position").first()
    position = last.position if last else 0
    for offset, (text, answers) in enumerate(QUESTIONS, 1):
        question, created = Question.objects.get_or_create(text=text, defaults={"position": position + offset})
        if created:
            for order, (answer, points) in enumerate(answers, 1):
                Answer.objects.create(question=question, text=answer, points=points, position=order)


class Migration(migrations.Migration):
    dependencies = [("accounts", "0003_fill_test_questions")]
    operations = [migrations.RunPython(add_questions, migrations.RunPython.noop)]

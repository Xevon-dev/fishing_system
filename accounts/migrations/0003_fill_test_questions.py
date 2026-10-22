from django.db import migrations

QUESTIONS = [
    {
        "text": "Як часто ви ходите на риболовлю?",
        "answers": [
            ("Кілька разів на рік", 1),
            ("Раз на місяць", 2),
            ("Кілька разів на місяць", 3),
            ("Щотижня або частіше", 4),
        ],
    },
    {
        "text": "Чи записуєте ви свої улови?",
        "answers": [
            ("Ні, ніколи", 1),
            ("Іноді записую", 2),
            ("Часто записую", 3),
            ("Так, веду детальний журнал", 4),
        ],
    },
    {
        "text": "Як ви зазвичай запам'ятовуєте інформацію про риболовлю?",
        "answers": [
            ("Просто запам'ятовую", 1),
            ("Роблю фотографії", 2),
            ("Записую в нотатки або блокнот", 3),
            ("Використовую таблиці або спеціальні застосунки", 4),
        ],
    },
    {
        "text": "Чи аналізуєте ви результати попередніх риболовель?",
        "answers": [
            ("Ні, не аналізую", 1),
            ("Іноді згадую, що спрацювало", 2),
            ("Порівнюю улови та умови риболовлі", 3),
            ("Регулярно аналізую свої результати", 4),
        ],
    },
]


def fill_questions(apps, schema_editor):
    TestQuestions = apps.get_model("accounts", "TestQuestions")
    TestAnswers = apps.get_model("accounts", "TestAnswers")

    for question_position, item in enumerate(QUESTIONS, start=1):
        question = TestQuestions.objects.create(
            text=item["text"],
            position=question_position,
        )

        for answer_position, (text, points) in enumerate(item["answers"], start=1):
            TestAnswers.objects.create(
                question=question,
                text=text,
                points=points,
                position=answer_position,
            )


def clear_questions(apps, schema_editor):
    TestQuestions = apps.get_model("accounts", "TestQuestions")
    TestQuestions.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_testquestions_testanswers"),
    ]

    operations = [
        migrations.RunPython(fill_questions, clear_questions),
    ]

def calculate_score(questions, answers):
    score = 0

    for question in questions:
        user_answer = answers.get(f"q{question['id']}")

        for answer in question["answers"]:
            if answer["id"] == user_answer:
                score += answer["points"]
                break

    return score


def get_fishing_level(score):
    if score <= 7:
        return "beginner", "Початківець"
    elif score <= 12:
        return "intermediate", "Середній"
    else:
        return "advanced", "Досвідчений"
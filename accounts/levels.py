LEVEL_NAMES = {
    "beginner": "Початківець",
    "intermediate": "Середній",
    "advanced": "Досвідчений",
}


def level_from_score(score, question_count=4):
    if question_count <= 0:
        return "beginner"
    if score <= 7 * question_count / 4:
        return "beginner"
    if score <= 12 * question_count / 4:
        return "intermediate"
    return "advanced"

LEVEL_NAMES = {
    "beginner": "Початківець",
    "intermediate": "Середній",
    "advanced": "Досвідчений",
}


def level_from_score(score):
    if score <= 7:
        return "beginner"
    if score <= 12:
        return "intermediate"
    return "advanced"

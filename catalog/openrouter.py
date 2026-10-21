

import requests
from django.conf import settings


def query_openrouter(prompt: str) -> str:
    api_key = settings.OPENROUTER_API

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(url, headers=headers, json=data, timeout=120)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]

    return f"Помилка: {response.status_code}, {response.text}"


if __name__ == "__main__":
    import os
    import sys

    import django

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    user_prompt = input("Введіть ваш промпт: ")
    answer = query_openrouter(user_prompt)
    print("\nВідповідь від openrouter.ai:")
    print(answer)

# Золота Рибка

Сайт для рибалок: тут можна зберігати риболовні сесії та улови, дивитися водойми й читати поради.

## Як запустити

1. Створи й активуй віртуальне середовище:

   ```powershell
   py -3.13 -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Встанови потрібні пакети:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Створи базу даних MySQL 8.4.11. Скопіюй приклад змінних у `.env`:

   ```powershell
   Copy-Item .env.example .env
   ```

   Відкрий `.env` і заповни дані бази та `SECRET_KEY`. Ключі Google Maps, Weather і OpenRouter можна додати за потреби.

4. Виконай міграції та запусти сайт:

   ```powershell
   python manage.py migrate
   python manage.py seed_demo_data
   python manage.py runserver
   ```

   Команда створить вигадані демо-сесії, улови та акаунт для входу. Повторний запуск не створює копії цих записів. Використовуй її лише для локальної демонстрації, не на production-сервері.

5. Відкрий у браузері `http://127.0.0.1:8000/`.

Проєкт використовує Django 5.2.18 і MySQL 8.4.11. Файл `.env` не додавай у Git.

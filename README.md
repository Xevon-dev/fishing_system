# Золота Рибка

Сайт для рибалок: сесії та улови, карта водойм, підбір снастей і поради.

Використано Python 3.13, Django 5.2.18 і MySQL 8.4.11.

## Як запустити

Виконуй команди в PowerShell у папці проєкту.

1. Створи середовище та встанови пакети:

   ```powershell
   py -3.13 -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

2. Запусти MySQL і створи базу в його консолі:

   ```sql
   CREATE DATABASE fishing_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. Для першого запуску створи файл налаштувань:

   ```powershell
   Copy-Item .env.example .env
   ```

   У `.env` заповни `SECRET_KEY` та дані MySQL: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`. Локально: назва бази — `fishing_system`, адреса — `127.0.0.1`, порт — `3306`.

   Ключі сервісів можна заповнити пізніше. Порожні рядки з `.env.example` не видаляй. Файл `.env` не додавай у Git.

4. Створи таблиці та запусти сайт:

   ```powershell
   python manage.py migrate
   python manage.py check
   python manage.py runserver
   ```

5. Відкрий `http://127.0.0.1:8000/` та зареєструйся.

## Ключі сервісів у `.env`

- `GOOGLE_MAPS_API_KEY` — карта.
- `WEATHER_API` — погода.
- `OPENROUTER_API` і `OPENROUTER_MODEL` — поради ШІ. Модель, наприклад: `openai/gpt-4o-mini`.
- `GOOGLE_OAUTH2_KEY` і `GOOGLE_OAUTH2_SECRET` — вхід через Google.

Адреса повернення для Google OAuth: `http://127.0.0.1:8000/social-auth/complete/google-oauth2/`.

## Дані для демонстрації

```powershell
python manage.py seed_demo_data
```

Команда додає приклади сесій, уловів і порад. Логін: `demo_fisher`, пароль: `DemoFish123`. Повторний запуск відновлює цей пароль. Дані водойм для карти завантажуються окремо.

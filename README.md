# Золота Рибка

Сайт для рибалок: сесії та улови, карта водойм, підбір снастей і поради.

Використано Python 3.13, Django 5.2.18 і PostgreSQL.

## Як запустити

Виконуй команди в PowerShell у папці проєкту.

1. Створи середовище та встанови пакети:

   ```powershell
   py -3.13 -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

2. Запусти PostgreSQL і створи базу:

   ```sql
   CREATE DATABASE fishing_system;
   ```

3. Для першого запуску створи файл налаштувань:

   ```powershell
   Copy-Item .env.example .env
   ```

   У `.env` заповни `SECRET_KEY` та PostgreSQL-змінні `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`. Локально: база — `fishing_system`, адреса — `127.0.0.1`, порт — `5432`. Для хостингу можна вказати повний рядок підключення в `DATABASE_URL`.

   Ключі сервісів можна заповнити пізніше. Порожні рядки з `.env.example` не видаляй. Файл `.env` не додавай у Git.

4. Створи таблиці та запусти сайт:

   ```powershell
   python manage.py migrate
   python manage.py check
   python manage.py runserver
   ```

   Якщо переходиш із MySQL і хочеш зберегти наявні записи, їх потрібно окремо експортувати з MySQL та імпортувати в PostgreSQL. `migrate` створює схему й початкові дані, але сам дані з MySQL не переносить.

5. Відкрий `http://127.0.0.1:8000/` та зареєструйся.

## Деплой на Render + Neon

1. Створи PostgreSQL-проєкт у Neon і скопіюй його connection string.
2. Завантаж репозиторій у GitHub та створи на Render новий Web Service з цього репозиторію. Render використає `render.yaml` для команд збірки й запуску.
3. У змінних середовища Render задай `DATABASE_URL` (Neon connection string) та `SECRET_KEY`. Додай ключі сервісів, якщо вони потрібні.
4. Після деплою Render автоматично виконає `collectstatic` і `migrate`.

Безкоштовний Render може засинати після періоду без запитів. Файли, завантажені користувачами (фото профілів, уловів і порад), на файловій системі Render не є постійними; для їх збереження потрібне зовнішнє сховище, наприклад Cloudinary. Фото з локальної папки `media/` також не переносяться автоматично.

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

import re

from .models import Users

EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
USERNAME_RE = re.compile(r"[\w\s'’\-]+")


def username_error(username):
    if not username:
        return "Введіть ім'я користувача"
    if len(username) < 3:
        return "Мінімум 3 символи"
    if len(username) > 150:
        return "Ім'я занадто довге"
    if not USERNAME_RE.fullmatch(username):
        return "Використовуйте літери, цифри, пробіли, апостроф або дефіс"
    return None


def email_error(email):
    if not email:
        return "Введіть електронну пошту"
    if not EMAIL_RE.fullmatch(email):
        return "Некоректна електронна пошта"
    if Users.objects.filter(email=email).exists():
        return "Така пошта вже зареєстрована"
    return None


def password_errors(password, confirm_password):
    errors = {}

    if not password:
        errors["password"] = "Введіть пароль"
    elif len(password) < 6:
        errors["password"] = "Мінімум 6 символів"

    if not confirm_password:
        errors["confirm_password"] = "Підтвердіть пароль"
    elif password != confirm_password:
        errors["confirm_password"] = "Паролі не збігаються"

    return errors

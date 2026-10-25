import re

from .models import Users

LOCAL_RE = re.compile(r"[a-z0-9._%+-]+")
LABEL_RE = re.compile(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
USERNAME_RE = re.compile(r"[\w\s'’\-]+")
UPPER_RE = re.compile(r"[A-ZА-ЯІЇЄ]")
LOWER_RE = re.compile(r"[a-zа-яіїє]")
DIGIT_RE = re.compile(r"\d")


def username_error(username, exclude_user_id=None):
    if not username:
        return "Введіть ім'я користувача"
    if len(username) < 3:
        return "Мінімум 3 символи"
    if len(username) > 150:
        return "Ім'я занадто довге"
    if not USERNAME_RE.fullmatch(username):
        return "Використовуйте літери, цифри, пробіли, апостроф або дефіс"

    taken = Users.objects.filter(username__iexact=username)

    if exclude_user_id:
        taken = taken.exclude(user_id=exclude_user_id)

    if taken.exists():
        return "Такий логін уже зайнятий"

    return None


def email_error(email, exclude_user_id=None):
    if not email:
        return "Введіть електронну пошту"

    email = email.strip().lower()

    if len(email) > 254 or email.count("@") != 1:
        return "Некоректна електронна пошта"

    local, _, domain = email.partition("@")

    if (
        not local
        or len(local) > 64
        or local.startswith(".")
        or local.endswith(".")
        or ".." in local
        or not LOCAL_RE.fullmatch(local)
    ):
        return "Некоректна електронна пошта"

    labels = domain.split(".")

    if (
        len(domain) > 253
        or len(labels) < 2
        or any(
            not label or label.startswith("-") or label.endswith("-")
            for label in labels
        )
        or not all(LABEL_RE.fullmatch(label) for label in labels)
        or len(labels[-1]) < 2
        or not labels[-1].isalpha()
    ):
        return "Некоректна електронна пошта"

    if Users.objects.filter(email__iexact=email).exclude(user_id=exclude_user_id).exists():
        return "Така пошта вже зареєстрована"

    return None


def password_strength_error(password, username="", email=""):
    if not password:
        return "Введіть пароль"
    if len(password) < 6:
        return "Мінімум 6 символів"
    if len(password) > 128:
        return "Пароль занадто довгий"
    if len(set(password)) == 1:
        return "Пароль не може складатися з однакових символів"
    if not (UPPER_RE.search(password) and LOWER_RE.search(password) and DIGIT_RE.search(password)):
        return "Додайте велику літеру, малу літеру та цифру"
    if username and username.lower() in password.lower():
        return "Пароль не повинен містити ваш логін"
    if email and email.partition("@")[0] in password.lower():
        return "Пароль не повинен містити адресу вашої пошти"
    return None


def password_errors(password, confirm_password, username="", email=""):
    errors = {}

    message = password_strength_error(password, username, email)
    if message:
        errors["password"] = message

    if not confirm_password:
        errors["confirm_password"] = "Підтвердіть пароль"
    elif password and password != confirm_password:
        errors["confirm_password"] = "Паролі не збігаються"

    return errors

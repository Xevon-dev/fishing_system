from django.contrib.auth.hashers import is_password_usable
from social_core.exceptions import AuthForbidden

from .models import Users
from .session import login_user


def sync_custom_user(backend, user, response, details, strategy, **kwargs):

    email = (details.get('email') or getattr(user, 'email', '')).strip().lower()
    if not email:
        raise AuthForbidden(backend, 'Google did not provide an email address.')

    custom_user = Users.objects.filter(email__iexact=email).first()
    if custom_user is None:
        strategy.request.session["google_registration_required"] = True
        raise AuthForbidden(backend, 'Спершу створіть обліковий запис на сайті.')

    if not is_password_usable(custom_user.password_hash):
        strategy.request.session["google_registration_required"] = True
        strategy.request.session["google_registration_user_id"] = custom_user.user_id
        raise AuthForbidden(backend, 'Спершу завершіть реєстрацію на сайті.')

    login_user(strategy.request, custom_user)
    if custom_user.level_id is None:
        strategy.request.session["google_level_required"] = True

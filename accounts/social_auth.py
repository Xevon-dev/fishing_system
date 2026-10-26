from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from .models import Users
from .session import login_user


def sync_custom_user(backend, user, response, details, strategy, **kwargs):

    email = (details.get('email') or getattr(user, 'email', '')).strip().lower()
    if not email:
        raise PermissionDenied('Google did not provide an email address.')

    custom_user = Users.objects.filter(email__iexact=email).first()
    if custom_user is None:
        username = (details.get('username') or details.get('fullname') or email.split('@', 1)[0])
        username = username.strip()[:45] or email.split('@', 1)[0][:45]
        custom_user = Users.objects.create(
            username=username,
            email=email,
            password_hash=make_password(None),
            created_at=timezone.now(),
        )

    login_user(strategy.request, custom_user)

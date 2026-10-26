from django.contrib.auth.models import AnonymousUser

from .session import current_user


class SessionUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = current_user(request)
        if user is not None:
            request.user = user
        elif not request.user.is_authenticated:
            request.user = AnonymousUser()
        return self.get_response(request)

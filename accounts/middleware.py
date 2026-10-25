from django.contrib.auth.models import AnonymousUser

from .session import current_user


class SessionUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            user = current_user(request)
            request.user = user or AnonymousUser()
        return self.get_response(request)

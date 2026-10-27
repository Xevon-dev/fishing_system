from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import is_password_usable
from django.shortcuts import redirect
from django.urls import reverse

from .session import current_user


class SessionUserMiddleware:
    public_views = {
        "catalog:home",
        "accounts:login",
        "accounts:register",
        "accounts:fishing_test",
        "social_complete",
    }
    public_namespaces = {"social", "admin"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = current_user(request)
        if user is not None:
            request.user = user
        elif not request.user.is_authenticated:
            request.user = AnonymousUser()
        return self.get_response(request)

    def is_asset_request(self, request):
        for asset_url in (settings.STATIC_URL, settings.MEDIA_URL):
            path = urlsplit(asset_url or "").path
            if path and request.path_info.startswith("/" + path.strip("/") + "/"):
                return True
        return False

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.session.get("google_level_required"):
            user = getattr(request, "_fishwise_current_user", None)
            if user and not is_password_usable(user.password_hash):
                request.session["google_registration_required"] = True
                request.session["google_registration_user_id"] = user.user_id
                request.session.pop("google_level_required", None)
                request.session.pop("user_id", None)
                request._fishwise_current_user = None
                request.user = AnonymousUser()
                return redirect(reverse("accounts:register"))
            allowed_views = {"accounts:google_level", "accounts:logout"}
            if request.resolver_match and request.resolver_match.view_name in allowed_views:
                return None
            if self.is_asset_request(request):
                return None
            return redirect(reverse("accounts:google_level"))

        if getattr(request, "_fishwise_current_user", None) is not None:
            return None

        match = request.resolver_match
        if match and (
            match.view_name in self.public_views
            or self.public_namespaces.intersection(match.namespaces)
        ):
            return None
        if self.is_asset_request(request):
            return None
        return redirect(reverse("accounts:login"))

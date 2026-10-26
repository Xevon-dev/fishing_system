from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from social_core.exceptions import AuthCanceled, AuthForbidden
from social_django.views import complete as social_complete
from ..session import logout_user


def social_auth_complete(request, backend):

    try:
        response = social_complete(request, backend=backend)
        if request.session.get("google_level_required"):
            return redirect(reverse("accounts:google_level"))
        return response
    except AuthForbidden:
        logout_user(request)
        return redirect("accounts:register")
    except AuthCanceled:
        messages.info(request, "Вхід через Google скасовано.")
        return redirect("accounts:login")

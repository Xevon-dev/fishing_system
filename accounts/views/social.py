from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.urls import reverse
from social_core.exceptions import AuthAlreadyAssociated, AuthCanceled, AuthForbidden
from social_django.views import complete as social_complete


def social_auth_complete(request, backend):
    # The app keeps its own Users session, separate from Django's auth user.
    # Don't let that custom user be treated as an account to associate with
    # the Google identity; the pipeline resolves the app account by email.
    request._fishwise_current_user = None
    request.user = AnonymousUser()
    try:
        response = social_complete(request, backend=backend)
        if request.session.get("google_level_required"):
            return redirect(reverse("accounts:google_level"))
        return response
    except AuthForbidden:
        request.session.pop("user_id", None)
        return redirect("accounts:register")
    except AuthAlreadyAssociated:
        messages.error(
            request,
            "Цей Google-акаунт уже прив’язаний до іншого профілю. "
            "Увійдіть у відповідний профіль або зверніться до підтримки.",
        )
        return redirect("accounts:login")
    except AuthCanceled:
        messages.info(request, "Вхід через Google скасовано.")
        return redirect("accounts:login")

from django.contrib import messages
from django.shortcuts import redirect
from social_core.exceptions import AuthCanceled
from social_django.views import complete as social_complete


def social_auth_complete(request, backend):

    try:
        return social_complete(request, backend=backend)
    except AuthCanceled:
        messages.info(request, "Вхід через Google скасовано.")
        return redirect("accounts:login")

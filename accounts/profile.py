"""Сторінка профілю рибака."""

from django.shortcuts import redirect, render

from journal.models import Catches, FishingTrips, Tips
from .session import current_user


def profile_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

    return render(request, "profile.html", {
        "profile_user": user,
        "trips": (
            FishingTrips.objects
            .filter(user_id=user.user_id)
            .select_related("water_body")
            .order_by("-start_time")[:10]
        ),
        "catches": (
            Catches.objects
            .filter(trip__user_id=user.user_id)
            .select_related("fish", "trip")
            .order_by("-catch_id")[:10]
        ),
        "tips": (
            Tips.objects
            .filter(author_id=user.user_id)
            .select_related("fish")
            .order_by("-tip_id")[:10]
        ),
    })

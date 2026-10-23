from django.shortcuts import redirect, render

from journal.models import FishingTrips, Tips
from ..session import current_user


def is_expert(user):
    return bool(user.level and user.level.name == "Досвідчений")


def profile_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

    tips = []
    if is_expert(user):
        tips = (
            Tips.objects
            .filter(author_id=user.user_id)
            .select_related("fish")
            .order_by("-tip_id")[:10]
        )

    return render(request, "profile.html", {
        "profile_user": user,
        "is_expert": is_expert(user),
        "trips": (
            FishingTrips.objects
            .filter(user_id=user.user_id)
            .select_related("water_body", "type", "method")
            .prefetch_related("catches_set__fish")
            .order_by("-created_at")[:10]
        ),
        "tips": tips,
    })

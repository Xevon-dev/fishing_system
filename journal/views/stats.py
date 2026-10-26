from django.db.models import Count, Sum
from django.shortcuts import redirect, render

from ..common import current_user
from ..models import Catches, FishingTrips


def stats_view(request):
    user = current_user(request)
    if not user:
        return redirect("accounts:login")

    trips = FishingTrips.objects.filter(user_id=user.user_id)
    catches = Catches.objects.filter(trip__user_id=user.user_id)

    total_weight = catches.aggregate(total=Sum("weight_kg"))["total"] or 0
    top_fish = (
        catches.values("fish__name")
        .annotate(total=Count("catch_id"))
        .order_by("-total")[:5]
    )
    weighted_catches = (
        catches.filter(fish__isnull=False, weight_kg__isnull=False)
        .select_related("fish", "trip", "trip__water_body", "trip__type", "trip__method")
        .order_by("fish_id", "-weight_kg", "-caught_at", "-catch_id")
    )
    trophies = []
    seen_fish = set()
    for catch in weighted_catches:
        if catch.fish_id in seen_fish:
            continue
        seen_fish.add(catch.fish_id)
        trophies.append(catch)

    successful_trips = trips.filter(catches__isnull=False).distinct().count()
    success_rate = round(successful_trips * 100 / trips.count()) if trips.exists() else 0

    return render(request, "stats.html", {
        "total_trips": trips.count(),
        "total_catches": catches.count(),
        "total_weight": total_weight,
        "top_fish": top_fish,
        "trophies": trophies,
        "trophy_count": len(trophies),
        "successful_trips": successful_trips,
        "success_rate": success_rate,
    })

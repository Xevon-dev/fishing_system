from django.db.models import Count, Sum
from django.shortcuts import redirect, render

from .common import current_user
from .models import Catches, FishingTrips


def stats_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

    trips = FishingTrips.objects.filter(user_id=user.user_id)
    catches = Catches.objects.filter(trip__user_id=user.user_id)

    total_weight = catches.aggregate(total=Sum("weight_kg"))["total"] or 0
    top_fish = (
        catches.values("fish__name")
        .annotate(total=Count("catch_id"))
        .order_by("-total")[:5]
    )

    return render(request, "stats.html", {
        "total_trips": trips.count(),
        "total_catches": catches.count(),
        "total_weight": total_weight,
        "top_fish": top_fish,
    })

from django.db.models import Count, Sum
from django.shortcuts import redirect, render
from django.utils import timezone

from accounts.models import Users
from catalog.models import FishSpecies
from .models import Catches, FishingTrips, Tips


def _current_user(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return Users.objects.select_related("level").filter(pk=user_id).first()


def tips_list_view(request):
    tips = Tips.objects.select_related("fish", "author").order_by("-tip_id")
    return render(request, "tips_list.html", {"tips": tips})


def journal_view(request):
    user = _current_user(request)
    if not user:
        return redirect("login")

    trips = (
        FishingTrips.objects
        .filter(user_id=user.user_id)
        .select_related("water_body")
        .prefetch_related("catches_set__fish", "catches_set__tackle")
        .order_by("-start_time")
    )
    return render(request, "journal.html", {"trips": trips})


def stats_view(request):
    user = _current_user(request)
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


def add_tip_view(request):
    user = _current_user(request)
    if not user:
        return redirect("login")

    # Додавати поради можуть лише досвідчені
    if not user.level or user.level.name != "Досвідчений":
        return render(request, "add_tip.html", {"not_allowed": True})

    errors = {}
    content = ""
    fish_id = ""

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        fish_id = request.POST.get("fish", "")

        if not content:
            errors["content"] = "Введіть текст поради"
        elif len(content) < 10:
            errors["content"] = "Мінімум 10 символів"

        if not errors:
            fish_obj = None
            if fish_id:
                fish_obj = FishSpecies.objects.filter(pk=fish_id).first()

            Tips.objects.create(
                author=user,
                fish=fish_obj,
                content=content,
                created_at=timezone.now(),
            )
            return redirect("tips_list")

    return render(request, "add_tip.html", {
        "errors": errors,
        "content": content,
        "fish_id": fish_id,
        "fish_list": FishSpecies.objects.all().order_by("name"),
    })

from django.shortcuts import render
from django.db.models import Count
from urllib.parse import quote_plus

from ..models import FishCategory, FishSpecies


def fish_advice_view(request):
    fish_list = (
        FishSpecies.objects
        .prefetch_related("categories")
        .distinct()
        .order_by("name")
    )
    for fish in fish_list:
        fish.fishing_info_link = fish.fishing_info_url or (
            "https://www.google.com/search?q="
            + quote_plus(f"{fish.name} коли ловити нерест")
        )
    fish_categories = (
        FishCategory.objects
        .annotate(fish_count=Count("fish"))
        .filter(fish_count__gt=0)
        .order_by("id")
    )
    return render(request, "fish_advice.html", {
        "fish_list": fish_list,
        "fish_categories": fish_categories,
    })

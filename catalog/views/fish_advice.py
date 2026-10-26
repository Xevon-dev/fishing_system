from django.db.models import Count
from django.views.generic import ListView
from urllib.parse import quote_plus

from ..models import FishCategory, FishSpecies


class FishSpeciesListView(ListView):
    model = FishSpecies
    template_name = "fish_advice.html"
    context_object_name = "fish_list"

    def get_queryset(self):
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
        return fish_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fish_categories"] = (
            FishCategory.objects
            .annotate(fish_count=Count("fish"))
            .filter(fish_count__gt=0)
            .order_by("id")
        )
        return context


fish_advice_view = FishSpeciesListView.as_view()

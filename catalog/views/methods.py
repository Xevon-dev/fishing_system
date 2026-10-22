"""Техніки лову: типи ловлі, їхні риби та способи."""

from django.db.models import Prefetch
from django.shortcuts import render

from ..models import FishSpecies, FishingMethods, FishingTypes


def methods_view(request):
    groups = []
    types = (
        FishingTypes.objects
        .prefetch_related(Prefetch("fish", queryset=FishSpecies.objects.order_by("name")))
        .order_by("type_id")
    )

    for fishing_type in types:
        methods = (
            FishingMethods.objects
            .filter(type=fishing_type)
            .order_by("method_id")
        )
        groups.append({
            "type": fishing_type,
            "fish": [fish.name for fish in fishing_type.fish.all()],
            "methods": list(methods),
        })

    return render(request, "methods.html", {"groups": groups})

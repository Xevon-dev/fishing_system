from django.shortcuts import get_object_or_404, redirect, render

from accounts.session import current_user

from ..models import FishSpecies, FishingTypes, Tackle, TackleSets

TACKLE_TIERS = ("дешеві", "середні", "дорогі")
TACKLE_KINDS = ("вудлище", "котушка", "приманка", "годівниця", "поплавок")
TACKLE_LIMIT = 6


def tackle_view(request, fish_id=None):
    user = current_user(request)

    if not user:
        return redirect("login")

    if not user.is_beginner:
        return redirect("methods")

    fish_list = (
        FishSpecies.objects
        .filter(fishingtypes__tackle__isnull=False)
        .distinct()
        .order_by("name")
    )

    fish = None
    groups = []
    tier = request.GET.get("tier", TACKLE_TIERS[0])

    if tier not in TACKLE_TIERS:
        tier = TACKLE_TIERS[0]

    if fish_id:
        fish = get_object_or_404(FishSpecies, pk=fish_id)
        types = FishingTypes.objects.filter(fish=fish)

        items = list(
            Tackle.objects
            .filter(type__in=types, tier=tier)
            .order_by("price")
        )

        sets = list(
            TackleSets.objects
            .filter(type__in=types, tier=tier)
            .order_by("price")
        )

        for fishing_type in types:
            type_items = [item for item in items if item.type_id == fishing_type.type_id]

            if not type_items:
                continue

            kinds = []

            for kind in TACKLE_KINDS:
                kind_items = [item for item in type_items if item.kind == kind][:TACKLE_LIMIT]

                if kind_items:
                    kinds.append({"kind": kind, "items": kind_items})

            groups.append({
                "type": fishing_type.name,
                "kinds": kinds,
                "sets": [
                    item for item in sets if item.type_id == fishing_type.type_id
                ][:TACKLE_LIMIT],
            })

    return render(request, "tackle.html", {
        "fish_list": fish_list,
        "fish": fish,
        "groups": groups,
        "tiers": TACKLE_TIERS,
        "tier": tier,
    })

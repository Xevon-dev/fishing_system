from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from accounts.session import current_user

from ..models import FishSpecies, FishingTypes, Tackle, TackleSets

TACKLE_TIERS = ("дешеві", "середні", "дорогі")
TACKLE_KINDS = (
    "вудлище",
    "котушка",
    "приманка",
    "боблер",
    "силікон",
    "годівниця",
    "прикормка",
    "насадка",
    "бойл",
    "пелета",
    "монтаж",
    "оснащення",
    "поплавок",
)
TACKLE_LIMIT = 6
UNIVERSAL_KINDS = ("вудлище", "котушка")

TACKLE_ALIASES = {
    "Донна": "Фідерна",
    "З човна": "Спінінгова",
    "Нахлист": "Спінінгова",
}


def tackle_view(request, fish_id=None):
    user = current_user(request)

    if not user:
        return redirect("accounts:login")

    if not user.is_beginner:
        return redirect("catalog:methods")

    types_with_tackle = set(
        Tackle.objects.filter(type__isnull=False).values_list("type__name", flat=True)
    )
    shown_types = set(types_with_tackle)

    for alias, target in TACKLE_ALIASES.items():
        if target in types_with_tackle:
            shown_types.add(alias)

    fish_list = (
        FishSpecies.objects
        .filter(fishingtypes__name__in=shown_types)
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
        types = list(FishingTypes.objects.filter(fish=fish))

        wanted = {fishing_type.name for fishing_type in types}

        for fishing_type in types:
            if fishing_type.name in TACKLE_ALIASES:
                wanted.add(TACKLE_ALIASES[fishing_type.name])

        items = list(
            Tackle.objects
            .filter(type__name__in=wanted, tier=tier)
            .filter(
                Q(fish=fish)
                | (Q(fish__isnull=True) & Q(kind__in=UNIVERSAL_KINDS))
            )
            .distinct()
            .order_by("price")
        )

        sets = list(
            TackleSets.objects
            .filter(type__name__in=wanted, tier=tier)
            .filter(Q(fish__isnull=True) | Q(fish=fish))
            .distinct()
            .order_by("price")
        )

        items_by_type = {}
        for item in items:
            items_by_type.setdefault(item.type.name, []).append(item)

        sets_by_type = {}
        for item in sets:
            sets_by_type.setdefault(item.type.name, []).append(item)

        seen = set()

        for fishing_type in types:
            name = fishing_type.name
            source = name if items_by_type.get(name) else TACKLE_ALIASES.get(name, "")

            type_items = items_by_type.get(source, [])
            type_sets = sets_by_type.get(source, [])

            fresh_items = [item for item in type_items if item.url not in seen]
            fresh_sets = [item for item in type_sets if item.url not in seen]

            for item in fresh_items + fresh_sets:
                seen.add(item.url)

            if not fresh_items and not fresh_sets:
                continue

            kinds = []

            for kind in TACKLE_KINDS:
                kind_items = [item for item in fresh_items if item.kind == kind][:TACKLE_LIMIT]

                if kind_items:
                    kinds.append({"kind": kind, "items": kind_items})

            groups.append({
                "type": name,
                "kinds": kinds,
                "sets": fresh_sets[:TACKLE_LIMIT],
            })

    return render(request, "tackle.html", {
        "fish_list": fish_list,
        "fish": fish,
        "groups": groups,
        "tiers": TACKLE_TIERS,
        "tier": tier,
    })

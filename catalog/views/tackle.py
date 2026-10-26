from django.shortcuts import redirect
from django.db.models import Q
from django.views.generic import DetailView, ListView

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


def tackle_fish_queryset():
    types_with_tackle = set(
        Tackle.objects.filter(type__isnull=False).values_list("type__name", flat=True)
    )
    shown_types = set(types_with_tackle)

    for alias, target in TACKLE_ALIASES.items():
        if target in types_with_tackle:
            shown_types.add(alias)

    return (
        FishSpecies.objects
        .filter(fishingtypes__name__in=shown_types)
        .distinct()
        .order_by("name")
    )


def tackle_groups(fish, tier):
    groups = []
    if fish is not None:
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

    return groups


class BeginnerTackleMixin:
    template_name = "tackle.html"

    def dispatch(self, request, *args, **kwargs):
        user = current_user(request)
        if not user:
            return redirect("accounts:login")
        if not user.is_beginner:
            return redirect("catalog:methods")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fish = context.get("fish")
        tier = self.request.GET.get("tier", TACKLE_TIERS[0])
        if tier not in TACKLE_TIERS:
            tier = TACKLE_TIERS[0]
        if "fish_list" not in context:
            context["fish_list"] = tackle_fish_queryset()
        context.update({
            "fish": fish,
            "groups": tackle_groups(fish, tier),
            "tiers": TACKLE_TIERS,
            "tier": tier,
        })
        return context

    def post(self, request, *args, **kwargs):
        # Як і раніше, POST лише показує підбір, не змінюючи даних.
        return self.get(request, *args, **kwargs)


class FishTackleListView(BeginnerTackleMixin, ListView):
    model = FishSpecies
    context_object_name = "fish_list"

    def get_queryset(self):
        return tackle_fish_queryset()


class FishTackleDetailView(BeginnerTackleMixin, DetailView):
    model = FishSpecies
    context_object_name = "fish"
    pk_url_kwarg = "fish_id"

    def get_object(self, queryset=None):
        # Старий маршрут з fish_id=0 показував підбір без вибраної риби.
        if self.kwargs[self.pk_url_kwarg] == 0:
            return None
        return super().get_object(queryset)


tackle_view = FishTackleListView.as_view()
tackle_fish_view = FishTackleDetailView.as_view()

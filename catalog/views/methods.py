from django.db.models import Prefetch
from django.views.generic import ListView

from ..models import FishSpecies, FishingMethods, FishingTypes


class FishingTypesListView(ListView):
    model = FishingTypes
    template_name = "methods.html"

    def get_queryset(self):
        return (
            FishingTypes.objects
            .prefetch_related(Prefetch("fish", queryset=FishSpecies.objects.order_by("name")))
            .order_by("type_id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = []
        for fishing_type in self.object_list:
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
        context["groups"] = groups
        return context


methods_view = FishingTypesListView.as_view()

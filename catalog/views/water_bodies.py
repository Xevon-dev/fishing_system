from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from ..models import WaterBodies
from ..regions import region_choices

WATER_FIELDS = (
    "water_body_id", "name", "type", "area_km2", "depth", "fish_list",
    "description", "wikipedia", "source", "geometry",
)


def water_bodies_view(request):
    focus = None
    water_id = request.GET.get("water", "")
    if water_id.isdigit():
        focus = WaterBodies.objects.filter(pk=water_id).first()

    return render(request, "water_bodies.html", {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        "regions": region_choices(),
        "focus_water": focus,
    })


def build_geojson_feature(water_body):
    if not water_body["geometry"]:
        return None

    properties = {
        key: value
        for key, value in water_body.items()
        if key != "geometry" and value is not None
    }
    properties["area_km2"] = float(water_body["area_km2"] or 0)
    properties["fish"] = properties.pop("fish_list", "")

    return {
        "type": "Feature",
        "properties": properties,
        "geometry": water_body["geometry"],
    }


class WaterBodiesGeoJSONListView(ListView):
    model = WaterBodies
    http_method_names = ["get"]

    def get_queryset(self):
        return WaterBodies.objects.filter(region_slug=self.kwargs["region"]).values(*WATER_FIELDS)

    def render_to_response(self, context, **response_kwargs):
        features = []
        for water_body in context["object_list"]:
            feature = build_geojson_feature(water_body)
            if feature:
                features.append(feature)
        return JsonResponse({
            "type": "FeatureCollection",
            "features": features,
        }, **response_kwargs)


class WaterBodyGeoJSONDetailView(DetailView):
    model = WaterBodies
    pk_url_kwarg = "water_body_id"
    http_method_names = ["get"]

    def get_queryset(self):
        return WaterBodies.objects.values(*WATER_FIELDS)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        # Карта очікує порожню колекцію, а не 404, якщо водойми вже немає.
        return queryset.filter(pk=self.kwargs[self.pk_url_kwarg]).first()

    def render_to_response(self, context, **response_kwargs):
        water_body = context["object"]
        feature = build_geojson_feature(water_body) if water_body else None
        return JsonResponse({
            "type": "FeatureCollection",
            "features": [feature] if feature else [],
        }, **response_kwargs)


water_bodies_geojson = WaterBodiesGeoJSONListView.as_view()
water_body_geojson = WaterBodyGeoJSONDetailView.as_view()

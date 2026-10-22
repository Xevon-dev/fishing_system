from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

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


@require_GET
def water_bodies_geojson(request, region):
    water_bodies = WaterBodies.objects.filter(region_slug=region).values(*WATER_FIELDS)

    features = []
    for water_body in water_bodies:
        feature = build_geojson_feature(water_body)
        if feature:
            features.append(feature)

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features,
    })


@require_GET
def water_body_geojson(request, water_body_id):
    water_body = (
        WaterBodies.objects
        .filter(pk=water_body_id)
        .values(*WATER_FIELDS)
        .first()
    )
    feature = build_geojson_feature(water_body) if water_body else None

    return JsonResponse({
        "type": "FeatureCollection",
        "features": [feature] if feature else [],
    })

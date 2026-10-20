from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import FishSpecies, FishingMethods, Tackle, WaterBodies


def home(request):
    return render(request, "home.html")


def water_bodies_view(request):
    return render(request, "water_bodies.html", {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
    })


def fish_advice_view(request):
    fish_list = FishSpecies.objects.all().order_by("name")
    return render(request, "fish_advice.html", {"fish_list": fish_list})


def tackle_view(request):
    tackle_list = Tackle.objects.all().order_by("name")
    return render(request, "tackle.html", {"tackle_list": tackle_list})


def methods_view(request):
    methods = FishingMethods.objects.select_related("min_level").order_by("name")
    return render(request, "methods.html", {"methods": methods})


@require_GET
def water_bodies_geojson(request, region):
   
    water_bodies = WaterBodies.objects.filter(region_slug=region).values(
        "name", "type", "area_km2", "depth", "fish_list",
        "description", "wikipedia", "source", "geometry",
    )

    features = []

    for water_body in water_bodies:
        if not water_body["geometry"]:
            continue

        properties = {
            "name": water_body["name"],
            "type": water_body["type"],
            "area_km2": float(water_body["area_km2"] or 0),
        }

        if water_body["depth"]:
            properties["depth"] = water_body["depth"]
        if water_body["fish_list"]:
            properties["fish"] = water_body["fish_list"]
        if water_body["description"]:
            properties["description"] = water_body["description"]
        if water_body["wikipedia"]:
            properties["wikipedia"] = water_body["wikipedia"]
        if water_body["source"]:
            properties["source"] = water_body["source"]

        features.append({
            "type": "Feature",
            "properties": properties,
            "geometry": water_body["geometry"],
        })

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features,
    })

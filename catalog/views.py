from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from .advice import get_advice
from .models import FishSpecies, FishingMethods, Tackle, WaterBodies
from .regions import region_choices
from .weather import get_forecast


def home(request):
    return render(request, "home.html")


def water_bodies_view(request):
    return render(request, "water_bodies.html", {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        "regions": region_choices(),
    })


def fish_advice_view(request):
    fish_list = FishSpecies.objects.all().order_by("name")
    return render(request, "fish_advice.html", {"fish_list": fish_list})


def tackle_view(request):
    tackle_list = Tackle.objects.all().order_by("name")
    return render(request, "tackle.html", {"tackle_list": tackle_list})


def methods_view(request):
    methods = (
        FishingMethods.objects
        .select_related("type")
        .order_by("type_id", "method_id")
    )
    return render(request, "methods.html", {"methods": methods})


@require_GET
def water_bodies_geojson(request, region):
    water_bodies = WaterBodies.objects.filter(region_slug=region).values(
        "water_body_id", "name", "type", "area_km2", "depth", "fish_list",
        "description", "wikipedia", "source", "geometry",
    )

    features = []

    for water_body in water_bodies:
        if not water_body["geometry"]:
            continue

        properties = {
            key: value
            for key, value in water_body.items()
            if key != "geometry" and value is not None
        }
        properties["area_km2"] = float(water_body["area_km2"] or 0)
        properties["fish"] = properties.pop("fish_list", "")

        features.append({
            "type": "Feature",
            "properties": properties,
            "geometry": water_body["geometry"],
        })

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features,
    })

DAYS_UA = ("Сьогодні", "Завтра", "Післязавтра")

@require_GET
def weather_view(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    try:
        forecast = get_forecast(lat, lon)
    except Exception as error:
        return JsonResponse({"error": str(error)}, status=502)

    days = []

    for index, day_data in enumerate(forecast["forecast"]["forecastday"]):
        day = day_data["day"]
        hours = day_data["hour"]

        days.append({
            "label": DAYS_UA[index],
            "condition": day["condition"]["text"],
            "icon": "https:" + day["condition"]["icon"],
            "temp": round(day["avgtemp_c"]),
            "wind": round(day["maxwind_kph"]),
            "precip": day["totalprecip_mm"],
            "humidity": round(day["avghumidity"]),
            "pressure": round(hours[12]["pressure_mb"] * 0.750062),
        })

    return render(request, "weather_card.html", {"days": days})


@require_GET
def advice_view(request):
    water = {
        "lat": request.GET.get("lat"),
        "lon": request.GET.get("lon"),
        "name": request.GET.get("name", ""),
        "type": request.GET.get("type", ""),
        "area": request.GET.get("area", ""),
        "depth": request.GET.get("depth", ""),
        "fish": request.GET.get("fish", ""),
    }

    try:
        paragraphs = get_advice(water)
    except Exception as error:
        return JsonResponse(
            {"error": f"Не вдалося отримати рекомендацію: {error}"}, status=502
        )

    return render(request, "advice_card.html", {
        "title": "Рекомендація",
        "paragraphs": paragraphs,
    })

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from ..advice import get_advice
from ..weather import get_forecast

DAYS_UA = ("Сьогодні", "Завтра", "Післязавтра")

WIND_DIRECTIONS_UA = {
    "N": "Пн",
    "NNE": "Пн-Пн-Сх",
    "NE": "Пн-Сх",
    "ENE": "Сх-Пн-Сх",
    "E": "Сх",
    "ESE": "Сх-Пд-Сх",
    "SE": "Пд-Сх",
    "SSE": "Пд-Пд-Сх",
    "S": "Пд",
    "SSW": "Пд-Пд-Зх",
    "SW": "Пд-Зх",
    "WSW": "Зх-Пд-Зх",
    "W": "Зх",
    "WNW": "Зх-Пн-Зх",
    "NW": "Пн-Зх",
    "NNW": "Пн-Пн-Зх",
}


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
            "feels": round(hours[12]["feelslike_c"]),
            "wind": round(day["maxwind_kph"]),
            "wind_dir": WIND_DIRECTIONS_UA.get(
                hours[12]["wind_dir"], hours[12]["wind_dir"]
            ),
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
            {"error": f"Не вдалося отримати прогноз кльову: {error}"}, status=502
        )

    return render(request, "advice_card.html", {
        "title": "Рекомендація",
        "paragraphs": paragraphs,
    })

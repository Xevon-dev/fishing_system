from django.shortcuts import render

from ..models import WaterBodies


def home(request):
    water_count = WaterBodies.objects.count()

    return render(
        request,
        "home.html",
        {
            "water_count": water_count,
            "water_count_text": f"{water_count:,}".replace(",", " "),
        },
    )

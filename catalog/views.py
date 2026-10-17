from django.shortcuts import render

from .models import FishSpecies, FishingMethods, Tackle, WaterBodies


def home(request):
    return render(request, "home.html")


def water_bodies_view(request):
    water_bodies = WaterBodies.objects.all().order_by("name")
    return render(request, "water_bodies.html", {"water_bodies": water_bodies})


def fish_advice_view(request):
    fish_list = FishSpecies.objects.all().order_by("name")
    return render(request, "fish_advice.html", {"fish_list": fish_list})


def tackle_view(request):
    tackle_list = Tackle.objects.all().order_by("name")
    return render(request, "tackle.html", {"tackle_list": tackle_list})


def methods_view(request):
    methods = FishingMethods.objects.select_related("min_level").order_by("name")
    return render(request, "methods.html", {"methods": methods})

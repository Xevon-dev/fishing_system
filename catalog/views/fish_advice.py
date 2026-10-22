from django.shortcuts import render

from ..models import FishSpecies


def fish_advice_view(request):
    fish_list = FishSpecies.objects.all().order_by("name")
    return render(request, "fish_advice.html", {"fish_list": fish_list})

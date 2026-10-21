from django.shortcuts import redirect, render
from django.utils import timezone

from catalog.models import FishSpecies
from .common import current_user
from .models import Tips


def tips_list_view(request):
    tips = Tips.objects.select_related("fish", "author").order_by("-tip_id")
    return render(request, "tips_list.html", {"tips": tips})


def add_tip_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

    if not user.level or user.level.name != "Досвідчений":
        return render(request, "add_tip.html", {"not_allowed": True})

    errors = {}
    content = ""
    fish_id = ""

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        fish_id = request.POST.get("fish", "")

        if not content:
            errors["content"] = "Введіть текст поради"
        elif len(content) < 10:
            errors["content"] = "Мінімум 10 символів"

        if not errors:
            fish_obj = None
            if fish_id:
                fish_obj = FishSpecies.objects.filter(pk=fish_id).first()

            Tips.objects.create(
                author=user,
                fish=fish_obj,
                content=content,
                created_at=timezone.now(),
            )
            return redirect("tips_list")

    return render(request, "add_tip.html", {
        "errors": errors,
        "content": content,
        "fish_id": fish_id,
        "fish_list": FishSpecies.objects.all().order_by("name"),
    })

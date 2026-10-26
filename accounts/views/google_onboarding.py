from django.shortcuts import redirect, render

from ..levels import LEVEL_NAMES
from ..models import Levels
from ..session import current_user


def google_level_view(request):
    user = current_user(request)
    if not user:
        return redirect("accounts:login")
    if user.level_id:
        request.session.pop("google_level_required", None)
        return redirect("accounts:profile")

    error = ""
    if request.method == "POST":
        selected_level = request.POST.get("fishing_level", "")
        level_name = LEVEL_NAMES.get(selected_level)
        if level_name:
            user.level, _ = Levels.objects.get_or_create(name=level_name)
            user.save(update_fields=["level"])
            request.session.pop("google_level_required", None)
            return redirect("accounts:profile")
        error = "Обери свій рівень риболовлі, щоб продовжити."

    return render(request, "google_level.html", {
        "levels": LEVEL_NAMES,
        "error": error,
    })

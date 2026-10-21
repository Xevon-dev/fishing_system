from django.shortcuts import redirect, render
from django.utils import timezone

from .common import current_user
from .models import Tips
from .tip_check import check_tip


def validate_tip(title, content):
    errors = {}

    if not title:
        errors["title"] = "Введіть назву поради"
    elif len(title) < 10:
        errors["title"] = "Мінімум 10 символів"
    elif len(title) > 200:
        errors["title"] = "Максимум 200 символів"

    if not content:
        errors["content"] = "Введіть текст поради"

    if not errors:
        ok, reason = check_tip(title, content)
        if not ok:
            errors["content"] = reason

    return errors


def tips_list_view(request):
    tips = Tips.objects.select_related("fish", "author").order_by("-tip_id")
    return render(request, "tips_list.html", {"tips": tips})


def add_tip_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

    if not user.level or user.level.name != "Досвідчений":
        return render(request, "add_tip.html", {"not_allowed": True})

    title = ""
    content = ""
    errors = {}

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        errors = validate_tip(title, content)

        if not errors:
            Tips.objects.create(
                author=user,
                title=title,
                content=content,
                created_at=timezone.now(),
            )
            return redirect("tips_list")

    return render(request, "add_tip.html", {
        "errors": errors,
        "title": title,
        "content": content,
    })


def edit_tip_view(request, tip_id):
    user = current_user(request)
    if not user:
        return redirect("login")

    tip = Tips.objects.filter(pk=tip_id).first()
    if not tip or tip.author_id != user.user_id:
        return redirect("tips_list")

    title = tip.title
    content = tip.content
    errors = {}

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        errors = validate_tip(title, content)

        if not errors:
            tip.title = title
            tip.content = content
            tip.save(update_fields=["title", "content"])
            return redirect("tips_list")

    return render(request, "add_tip.html", {
        "tip": tip,
        "errors": errors,
        "title": title,
        "content": content,
    })

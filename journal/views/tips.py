from django.shortcuts import redirect, render
from django.db.models import Count, Exists, OuterRef, Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from catalog.models import FishSpecies
from accounts.image_uploads import image_upload_error
from ..common import current_user
from ..models import TipLike, Tips
from ..tip_check import MAX_LENGTH, check_tip


def validate_tip(title, content, fish_ids=(), photo=None, applies_to_all_fish=False):
    errors = {}
    selected_fishes = []

    if not title:
        errors["title"] = "Введіть назву поради"
    elif len(title) < 10:
        errors["title"] = "Мінімум 10 символів"
    elif len(title) > 200:
        errors["title"] = "Максимум 200 символів"

    if not content:
        errors["content"] = "Введіть текст поради"
    elif len(content) < 20:
        errors["content"] = "Опиши пораду детальніше — щонайменше 20 символів."
    elif len(content) > MAX_LENGTH:
        errors["content"] = f"Максимум {MAX_LENGTH} символів."

    if applies_to_all_fish:
        selected_fishes = list(FishSpecies.objects.order_by("name"))
        if not selected_fishes:
            errors["fishes"] = "У довіднику ще немає риб."
    else:
        try:
            selected_ids = [int(fish_id) for fish_id in fish_ids]
        except (TypeError, ValueError):
            selected_ids = []
            errors["fishes"] = "Обери риб зі списку."
        if not selected_ids:
            errors["fishes"] = "Виберіть хоча б одну рибу зі списку."
        elif len(set(selected_ids)) != len(selected_ids):
            errors["fishes"] = "Не обирайте одну рибу кілька разів."
        elif not errors:
            fish_by_id = FishSpecies.objects.in_bulk(selected_ids)
            if len(fish_by_id) != len(selected_ids):
                errors["fishes"] = "Виберіть рибу зі списку."
            else:
                selected_fishes = [fish_by_id[fish_id] for fish_id in selected_ids]

    photo_error = image_upload_error(photo)
    if photo_error:
        errors["photo"] = photo_error

    if not errors:
        ok, reason = check_tip(title, content)
        if not ok:
            errors["content"] = reason

    return errors, selected_fishes, applies_to_all_fish


def tips_list_view(request):
    user = current_user(request)
    tips = Tips.objects.select_related("fish", "author").prefetch_related("fishes").annotate(
        likes_count=Count("likes", filter=Q(likes__is_like=True), distinct=True),
        dislikes_count=Count("likes", filter=Q(likes__is_like=False), distinct=True),
    )
    if user:
        user_reactions = TipLike.objects.filter(tip_id=OuterRef("pk"), user=user)
        tips = tips.annotate(
            user_liked=Exists(user_reactions.filter(is_like=True)),
            user_disliked=Exists(user_reactions.filter(is_like=False)),
        )
    else:
        no_reaction = Exists(TipLike.objects.none())
        tips = tips.annotate(user_liked=no_reaction, user_disliked=no_reaction)
    sort = request.GET.get("sort", "newest")
    if sort == "popular":
        tips = tips.order_by("-likes_count", "dislikes_count", "-tip_id")
    elif sort == "worst":
        tips = tips.order_by("-dislikes_count", "likes_count", "tip_id")
    else:
        sort = "newest"
        tips = tips.order_by("-tip_id")
    return render(request, "tips_list.html", {"tips": tips, "sort": sort})


@require_POST
def toggle_tip_like_view(request, tip_id):
    user = current_user(request)
    if not user:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Увійдіть, щоб оцінювати поради."}, status=401)
        return redirect("login")
    is_like = request.POST.get("reaction") == "like"
    reaction = TipLike.objects.filter(tip_id=tip_id, user=user).first()
    if reaction and reaction.is_like == is_like:
        reaction.delete()
    elif Tips.objects.filter(pk=tip_id).exists():
        TipLike.objects.update_or_create(
            tip_id=tip_id,
            user=user,
            defaults={"is_like": is_like},
        )
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        reactions = TipLike.objects.filter(tip_id=tip_id)
        return JsonResponse({
            "likes": reactions.filter(is_like=True).count(),
            "dislikes": reactions.filter(is_like=False).count(),
            "reaction": (
                "like" if reactions.filter(user=user, is_like=True).exists()
                else "dislike" if reactions.filter(user=user, is_like=False).exists()
                else None
            ),
        })
    return redirect(request.POST.get("next") or "tips_list")


def add_tip_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

    if not user.level or user.level.name != "Досвідчений":
        return render(request, "add_tip.html", {"not_allowed": True})

    title = ""
    content = ""
    selected_fish_ids = []
    applies_to_all_fish = False
    errors = {}

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        submitted_fish_ids = request.POST.getlist("fishes")
        applies_to_all_fish = request.POST.get("applies_to_all_fish") == "1"
        for fish_id in submitted_fish_ids:
            try:
                selected_fish_ids.append(int(fish_id))
            except (TypeError, ValueError):
                pass
        uploaded_photos = request.FILES.getlist("photo")
        photo = uploaded_photos[0] if uploaded_photos else None
        errors, selected_fishes, applies_to_all_fish = validate_tip(
            title, content, submitted_fish_ids, photo, applies_to_all_fish
        )
        if len(uploaded_photos) > 1:
            errors["photo"] = "До поради можна додати лише одне зображення."

        if not errors:
            tip = Tips.objects.create(
                author=user,
                title=title,
                fish=selected_fishes[0],
                applies_to_all_fish=applies_to_all_fish,
                content=content,
                created_at=timezone.now(),
                photo=photo,
            )
            tip.fishes.set(selected_fishes)
            return redirect("tips_list")

    return render(request, "add_tip.html", {
        "errors": errors,
        "title": title,
        "content": content,
        "selected_fish_ids": selected_fish_ids,
        "applies_to_all_fish": applies_to_all_fish,
        "fish_options": FishSpecies.objects.order_by("name"),
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
    applies_to_all_fish = tip.applies_to_all_fish
    selected_fish_ids = (
        list(FishSpecies.objects.values_list("fish_id", flat=True))
        if applies_to_all_fish
        else list(tip.fishes.values_list("fish_id", flat=True))
    )
    if not selected_fish_ids and tip.fish_id:
        selected_fish_ids = [tip.fish_id]
    errors = {}

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        submitted_fish_ids = request.POST.getlist("fishes")
        applies_to_all_fish = request.POST.get("applies_to_all_fish") == "1"
        selected_fish_ids = []
        for fish_id in submitted_fish_ids:
            try:
                selected_fish_ids.append(int(fish_id))
            except (TypeError, ValueError):
                pass
        uploaded_photos = request.FILES.getlist("photo")
        photo = uploaded_photos[0] if uploaded_photos else None
        errors, selected_fishes, applies_to_all_fish = validate_tip(
            title, content, submitted_fish_ids, photo, applies_to_all_fish
        )
        if len(uploaded_photos) > 1:
            errors["photo"] = "До поради можна додати лише одне зображення."

        if not errors:
            if photo:
                if tip.photo:
                    tip.photo.delete(save=False)
                tip.photo = photo
            tip.title = title
            tip.fish = selected_fishes[0]
            tip.applies_to_all_fish = applies_to_all_fish
            tip.content = content
            tip.save(update_fields=["title", "fish", "content", "photo", "applies_to_all_fish"])
            tip.fishes.set(selected_fishes)
            return redirect("tips_list")

    return render(request, "add_tip.html", {
        "tip": tip,
        "errors": errors,
        "title": title,
        "content": content,
        "selected_fish_ids": selected_fish_ids,
        "applies_to_all_fish": applies_to_all_fish,
        "fish_options": FishSpecies.objects.order_by("name"),
    })


@require_POST
def delete_tip_view(request, tip_id):
    user = current_user(request)
    if not user:
        return redirect("login")

    tip = Tips.objects.filter(pk=tip_id, author_id=user.user_id).first()
    if not tip:
        return redirect("tips_list")

    next_url = request.POST.get("next") or ""
    tip.delete()

    if next_url and next_url.startswith("/") and not next_url.startswith("//"):
        return redirect(next_url)

    return redirect("tips_list")


@require_POST
def delete_tip_photo_view(request, tip_id):
    user = current_user(request)
    if not user:
        return redirect("login")

    tip = Tips.objects.filter(pk=tip_id, author_id=user.user_id).first()
    if tip and tip.photo:
        tip.photo.delete(save=False)
        tip.save(update_fields=["photo"])
    return redirect("edit_tip", tip_id=tip_id)

from django.conf import settings
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from catalog.models import FishSpecies, FishingTypes, WaterBodies
from catalog.regions import region_choices
from ..common import as_int, current_user
from ..models import Catches, FishingTripPhotos, FishingTrips
from .trip_form import form_defaults, parse_form
from ..catch_forms import CatchInlineFormSet
from accounts.image_uploads import image_upload_error


def journal_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

    trips = (
        FishingTrips.objects
        .filter(user_id=user.user_id)
        .select_related("water_body", "type", "method")
        .prefetch_related("catches_set__fish", "catches_set__tackle", "photos")
        .order_by("-created_at")
    )
    trip_count = catch_count = water_count = 0
    total_weight = 0
    seen_waters = set()
    for trip in trips:
        trip_count += 1
        seen_waters.add(trip.water_body_id)
        for catch in trip.catches_set.all():
            catch_count += catch.quantity or 1
            if catch.weight_kg:
                total_weight += catch.weight_kg * (catch.quantity or 1)
    water_count = len(seen_waters)
    return render(request, "journal.html", {
        "trips": trips,
        "trip_count": trip_count,
        "catch_count": catch_count,
        "water_count": water_count,
        "total_weight": total_weight,
    })


def trip_form_view(request, trip=None):
    user = current_user(request)
    if not user:
        return redirect("login")

    if request.method == "POST":
        form, errors, values = parse_form(request.POST, trip)
        instance = trip or FishingTrips(user=user)
        for field, value in values.items():
            setattr(instance, field, value)
        catches = CatchInlineFormSet(request.POST, request.FILES, instance=instance, prefix="catches")
        catches_valid = catches.is_valid()
        uploaded_photos = request.FILES.getlist("photos")
        photo_error = next((error for error in (image_upload_error(photo) for photo in uploaded_photos) if error), "")

        if not errors and catches_valid and not photo_error:
            with transaction.atomic():
                if trip:
                    instance.updated_at = timezone.now()
                else:
                    # Legacy start_time is retained for old database compatibility,
                    # but it is no longer a user-entered session time.
                    instance.start_time = timezone.now()
                instance.save()
                for uploaded_photo in uploaded_photos:
                    FishingTripPhotos.objects.create(trip=instance, photo=uploaded_photo)
                catches.save()
            return redirect("journal")

        selected_water = values["water_body"]
    else:
        form = form_defaults(trip)
        catches = CatchInlineFormSet(instance=trip or FishingTrips(user=user), prefix="catches")
        errors = {}

        water_body_id = as_int(form["water_body_id"])
        selected_water = None
        if water_body_id:
            selected_water = WaterBodies.objects.filter(pk=water_body_id).first()

    return render(request, "add_trip.html", {
        "trip": trip,
        "selected_water": selected_water,
        "errors": errors,
        "photo_error": photo_error if request.method == "POST" else "",
        "form": form,
        "catches": catches,
        "types": FishingTypes.objects.order_by("type_id"),
        "fish_options": FishSpecies.objects.order_by("name"),
        "regions": region_choices(),
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
    })


def add_trip_view(request):
    return trip_form_view(request)


def edit_trip_view(request, trip_id):
    user = current_user(request)
    if not user:
        return redirect("login")

    trip = FishingTrips.objects.filter(pk=trip_id, user_id=user.user_id).first()
    if not trip:
        return redirect("journal")

    return trip_form_view(request, trip)


@require_POST
def delete_trip_view(request, trip_id):
    user = current_user(request)
    if not user:
        return redirect("login")

    trip = FishingTrips.objects.filter(pk=trip_id, user_id=user.user_id).first()
    if trip:
        for trip_photo in trip.photos.all():
            trip_photo.photo.delete(save=False)
        Catches.objects.filter(trip_id=trip.trip_id).delete()
        trip.delete()

    return redirect("journal")


@require_POST
def delete_trip_photo_view(request, trip_id, photo_id):
    user = current_user(request)
    if not user:
        return redirect("login")

    trip = FishingTrips.objects.filter(pk=trip_id, user_id=user.user_id).first()
    if not trip:
        return redirect("journal")

    trip_photo = FishingTripPhotos.objects.filter(
        pk=photo_id,
        trip_id=trip.trip_id,
    ).first()
    if trip_photo:
        trip_photo.photo.delete(save=False)
        trip_photo.delete()

    return redirect("edit_trip", trip_id=trip.trip_id)

from django.conf import settings
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from catalog.models import FishingMethods, FishingTypes, WaterBodies
from catalog.regions import region_choices
from ..common import as_int, current_user
from ..models import Catches, FishingTrips
from .trip_form import form_defaults, parse_form
from ..catch_forms import CatchInlineFormSet


def journal_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

    trips = (
        FishingTrips.objects
        .filter(user_id=user.user_id)
        .select_related("water_body", "type", "method")
        .prefetch_related("catches_set__fish", "catches_set__tackle")
        .order_by("-created_at")
    )
    return render(request, "journal.html", {"trips": trips})


def trip_form_view(request, trip=None):
    user = current_user(request)
    if not user:
        return redirect("login")

    if request.method == "POST":
        form, errors, values = parse_form(request.POST, trip)
        instance = trip or FishingTrips(user=user)
        for field, value in values.items():
            setattr(instance, field, value)
        catches = CatchInlineFormSet(request.POST, instance=instance, prefix="catches")
        catches_valid = catches.is_valid()

        if not errors and catches_valid:
            with transaction.atomic():
                if trip:
                    instance.updated_at = timezone.now()
                else:
                    # Legacy start_time is retained for old database compatibility,
                    # but it is no longer a user-entered session time.
                    instance.start_time = timezone.now()
                instance.save()
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
        "form": form,
        "catches": catches,
        "types": FishingTypes.objects.order_by("type_id"),
        "methods": FishingMethods.objects.order_by("type_id", "method_id"),
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
        Catches.objects.filter(trip_id=trip.trip_id).delete()
        trip.delete()

    return redirect("journal")

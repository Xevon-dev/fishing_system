

from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

from django.utils import timezone

from catalog.models import FishingMethods, FishingTypes, WaterBodies
from ..common import as_int

FIELDS = (
    "water_body_id",
    "type",
    "method",
    "method_note",
    "bait_note",
    "fish_note",
    "start_time",
    "hours_spent",
    "note",
)


def form_defaults(trip=None):
    if trip:
        return {
            "water_body_id": str(trip.water_body_id),
            "type": str(trip.type_id or ""),
            "method": str(trip.method_id or ""),
            "method_note": trip.method_note or "",
            "bait_note": trip.bait_note or "",
            "fish_note": trip.fish_note or "",
            "start_time": timezone.localtime(trip.start_time).strftime("%Y-%m-%dT%H:%M"),
            "hours_spent": str(float(trip.hours_spent)) if trip.hours_spent else "",
            "note": trip.note or "",
        }

    return {
        "water_body_id": "",
        "type": "",
        "method": "",
        "method_note": "",
        "bait_note": "",
        "fish_note": "",
        "start_time": timezone.localtime().strftime("%Y-%m-%dT%H:%M"),
        "hours_spent": "",
        "note": "",
    }


def parse_start(value, errors):
    if not value:
        errors["start_time"] = "Вкажи дату й час початку"
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M")
    except ValueError:
        errors["start_time"] = "Невірний формат дати"
        return None


def parse_hours(value, errors):
    if not value:
        return None

    try:
        hours = Decimal(value)
    except InvalidOperation:
        errors["hours_spent"] = "Введи число годин"
        return None

    if hours < 0 or hours > 72:
        errors["hours_spent"] = "Тривалість — від 0 до 72 годин"
        return None

    return hours


def parse_form(post, trip=None):
    form = form_defaults(trip)
    for field in FIELDS:
        form[field] = post.get(field, "").strip()

    errors = {}

    water_body = None
    water_body_id = as_int(form["water_body_id"])
    if water_body_id:
        water_body = WaterBodies.objects.filter(pk=water_body_id).first()
    if not water_body:
        errors["water_body_id"] = "Обери водойму на карті"

    type_id = as_int(form["type"])
    if not type_id or not FishingTypes.objects.filter(pk=type_id).exists():
        errors["type"] = "Обери тип риболовлі"
        type_id = None

    method_id = as_int(form["method"])
    if method_id and not FishingMethods.objects.filter(pk=method_id).exists():
        method_id = None

    start = parse_start(form["start_time"], errors)
    hours = parse_hours(form["hours_spent"], errors)

    end = start + timedelta(hours=float(hours)) if start and hours else None

    values = {
        "water_body": water_body,
        "start_time": timezone.make_aware(start) if start else None,
        "end_time": timezone.make_aware(end) if end else None,
        "hours_spent": hours,
        "type_id": type_id,
        "method_id": method_id,
        "method_note": form["method_note"] or None,
        "bait_note": form["bait_note"] or None,
        "fish_note": form["fish_note"] or None,
        "note": form["note"] or None,
    }

    return form, errors, values

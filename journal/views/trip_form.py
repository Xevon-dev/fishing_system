

from catalog.models import FishingTypes, WaterBodies
from ..common import as_int

FIELDS = (
    "water_body_id",
    "type",
    "method_note",
    "note",
)


def form_defaults(trip=None):
    if trip:
        return {
            "water_body_id": str(trip.water_body_id),
            "type": str(trip.type_id or ""),
            "method_note": trip.method_note or (trip.method.name if trip.method_id else ""),
            "note": trip.note or "",
        }

    return {
        "water_body_id": "",
        "type": "",
        "method_note": "",
        "note": "",
    }


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

    if len(form["method_note"]) > 255:
        errors["method_note"] = "Максимум 255 символів."
    if len(form["note"]) > 3000:
        errors["note"] = "Нотатка має містити не більше 3 000 символів."

    values = {
        "water_body": water_body,
        "type_id": type_id,
        "method_id": None,
        "method_note": form["method_note"] or None,
        "note": form["note"] or None,
    }

    return form, errors, values

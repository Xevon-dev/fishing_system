import re
from decimal import Decimal, InvalidOperation

from django.db import migrations, models


WEIGHT_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:кг|kg)", re.IGNORECASE)


def preserve_legacy_catches(apps, schema_editor):
    FishingTrips = apps.get_model("journal", "FishingTrips")
    Catches = apps.get_model("journal", "Catches")
    FishSpecies = apps.get_model("catalog", "FishSpecies")
    fish_names = list(FishSpecies.objects.values_list("fish_id", "name"))

    for trip in FishingTrips.objects.exclude(
        fish_note__isnull=True,
        catch_weight_kg__isnull=True,
    ).iterator():
        legacy_note = (trip.fish_note or "").strip()
        matching_fish = [
            (fish_id, name)
            for fish_id, name in fish_names
            if legacy_note.casefold().startswith(name.casefold())
        ]
        fish_id = max(matching_fish, key=lambda pair: len(pair[1]))[0] if matching_fish else None
        weight = trip.catch_weight_kg
        if weight is None and legacy_note:
            match = WEIGHT_RE.search(legacy_note)
            if match:
                try:
                    weight = Decimal(match.group(1).replace(",", "."))
                except InvalidOperation:
                    weight = None

        if fish_id:
            Catches.objects.create(
                trip_id=trip.pk,
                fish_id=fish_id,
                weight_kg=weight,
                quantity=1,
            )
            continue

        preserved = legacy_note
        if trip.catch_weight_kg is not None:
            weight_note = f"Стара вага улову: {trip.catch_weight_kg} кг"
            preserved = f"{preserved}; {weight_note}" if preserved else weight_note
        if preserved:
            previous_note = (trip.note or "").strip()
            trip.note = f"{previous_note}\n{preserved}" if previous_note else preserved
            trip.save(update_fields=["note"])


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0010_fishspecies_image_source"),
        ("journal", "0003_catches_caught_at"),
    ]

    operations = [
        migrations.RunPython(preserve_legacy_catches, migrations.RunPython.noop),
        migrations.RemoveField(model_name="fishingtrips", name="fish_note"),
        migrations.RemoveField(model_name="fishingtrips", name="catch_weight_kg"),
    ]

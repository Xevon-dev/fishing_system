from django.db import migrations, models
from django.db.models import F


def initialize_trip_timestamps(apps, schema_editor):
    FishingTrips = apps.get_model("journal", "FishingTrips")
    # Creation/edit audit timestamps didn't exist before. Use the best
    # historical timestamp available and leave unknown edit times unset.
    FishingTrips.objects.filter(created_at__isnull=True).update(created_at=F("start_time"))


class Migration(migrations.Migration):
    dependencies = [("journal", "0004_remove_legacy_trip_catch_fields")]

    operations = [
        migrations.AddField(
            model_name="fishingtrips",
            name="created_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="fishingtrips",
            name="updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(initialize_trip_timestamps, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="fishingtrips",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

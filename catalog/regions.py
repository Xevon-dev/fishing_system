from django.db.models import Count

from .models import WaterBodies


def region_choices():
    return (
        WaterBodies.objects
        .exclude(region_slug="")
        .values("region_slug", "region")
        .annotate(total=Count("water_body_id"))
        .order_by("region")
    )

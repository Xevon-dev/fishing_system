from django.contrib import admin

from .models import (
    FishSpecies,
    FishingMethods,
    FishingTypes,
    Tackle,
    WaterBodies,
)


@admin.register(WaterBodies)
class WaterBodiesAdmin(admin.ModelAdmin):
    list_display = ("water_body_id", "name", "type", "region", "area_km2")
    list_filter = ("region_slug",)
    search_fields = ("name", "region")
    list_per_page = 50
    readonly_fields = ("geometry",)


@admin.register(FishSpecies)
class FishSpeciesAdmin(admin.ModelAdmin):
    list_display = ("fish_id", "name")
    search_fields = ("name",)


@admin.register(FishingTypes)
class FishingTypesAdmin(admin.ModelAdmin):
    list_display = ("type_id", "name")
    search_fields = ("name",)
    filter_horizontal = ("fish",)


@admin.register(FishingMethods)
class FishingMethodsAdmin(admin.ModelAdmin):
    list_display = ("method_id", "name", "type", "min_level")
    list_select_related = ("type", "min_level")
    search_fields = ("name",)


@admin.register(Tackle)
class TackleAdmin(admin.ModelAdmin):
    list_display = ("tackle_id", "name", "kind")
    list_filter = ("kind",)
    search_fields = ("name",)

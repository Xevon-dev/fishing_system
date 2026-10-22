from django.contrib import admin
from django.utils.html import format_html

from .models import (
    FishSpecies,
    FishingMethods,
    FishingTypes,
    Tackle,
    TackleSets,
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
    list_display = ("type_id", "name", "video")
    search_fields = ("name",)
    filter_horizontal = ("fish",)

    @admin.display(description="відео")
    def video(self, obj):
        if not obj.video_url:
            return "—"
        return format_html('<a href="{}" target="_blank">дивитись</a>', obj.video_url)


@admin.register(FishingMethods)
class FishingMethodsAdmin(admin.ModelAdmin):
    list_display = ("method_id", "name", "type", "min_level", "video")
    list_select_related = ("type", "min_level")
    search_fields = ("name",)

    @admin.display(description="відео")
    def video(self, obj):
        if not obj.video_url:
            return "—"
        return format_html('<a href="{}" target="_blank">дивитись</a>', obj.video_url)


@admin.register(Tackle)
class TackleAdmin(admin.ModelAdmin):
    list_display = ("tackle_id", "name", "kind", "type", "tier", "price", "shop", "link")
    list_filter = ("kind", "tier", "type", "shop")
    list_select_related = ("type",)
    search_fields = ("name",)

    @admin.display(description="магазин")
    def link(self, obj):
        if not obj.url:
            return "—"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">відкрити</a>', obj.url
        )


@admin.register(TackleSets)
class TackleSetsAdmin(admin.ModelAdmin):
    list_display = ("set_id", "name", "type", "tier", "price", "shop", "link")
    list_filter = ("tier", "type", "shop")
    list_select_related = ("type",)
    search_fields = ("name",)

    @admin.display(description="магазин")
    def link(self, obj):
        if not obj.url:
            return "—"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">відкрити</a>', obj.url
        )

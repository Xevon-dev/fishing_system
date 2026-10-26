from django.contrib import admin
from django.utils.text import Truncator
from django.utils.html import format_html

from .models import (
    FishSpecies,
    FishCategory,
    FishingMethods,
    FishingTypes,
    Tackle,
    TackleSets,
    WaterBodies,
)


@admin.register(FishCategory)
class FishCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(WaterBodies)
class WaterBodiesAdmin(admin.ModelAdmin):
    list_display = ("water_body_id", "name", "type", "region", "area_km2")
    list_filter = ("region_slug",)
    search_fields = ("name", "region")
    list_per_page = 50
    readonly_fields = ("geometry",)


@admin.register(FishSpecies)
class FishSpeciesAdmin(admin.ModelAdmin):
    list_display = (
        "fish_id",
        "name",
        "description_preview",
        "advice_preview",
        "wikipedia_link",
    )
    search_fields = ("name", "description", "advice")
    fields = ("name", "description", "advice", "image", "wikipedia", "fishing_info_url", "image_source", "categories")
    filter_horizontal = ("categories",)

    @admin.display(description="опис")
    def description_preview(self, obj):
        return Truncator(obj.description or "–").chars(70)

    @admin.display(description="порада")
    def advice_preview(self, obj):
        return Truncator(obj.advice or "–").chars(60)

    @admin.display(description="Вікіпедія")
    def wikipedia_link(self, obj):
        if not obj.wikipedia:
            return "–"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer">відкрити</a>',
            obj.wikipedia,
        )


@admin.register(FishingTypes)
class FishingTypesAdmin(admin.ModelAdmin):
    list_display = ("type_id", "name", "video")
    search_fields = ("name",)
    filter_horizontal = ("fish",)

    @admin.display(description="відео")
    def video(self, obj):
        if not obj.video_url:
            return "–"
        return format_html('<a href="{}" target="_blank">дивитись</a>', obj.video_url)


@admin.register(FishingMethods)
class FishingMethodsAdmin(admin.ModelAdmin):
    list_display = ("method_id", "name", "type", "min_level", "video")
    list_select_related = ("type", "min_level")
    search_fields = ("name",)

    @admin.display(description="відео")
    def video(self, obj):
        if not obj.video_url:
            return "–"
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
            return "–"
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
            return "–"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">відкрити</a>', obj.url
        )

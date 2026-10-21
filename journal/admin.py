from django.contrib import admin

from .models import Catches, FishingTrips, Tips


@admin.register(FishingTrips)
class FishingTripsAdmin(admin.ModelAdmin):
    list_display = ("trip_id", "user", "water_body", "start_time", "type", "method")
    list_select_related = ("user", "water_body", "type", "method")
    list_filter = ("type", "method")
    search_fields = ("water_body__name", "fish_note", "note")
    list_per_page = 50


@admin.register(Catches)
class CatchesAdmin(admin.ModelAdmin):
    list_display = ("catch_id", "trip", "fish", "weight_kg", "quantity", "tackle")
    list_select_related = ("trip", "fish", "tackle")
    list_per_page = 50


@admin.register(Tips)
class TipsAdmin(admin.ModelAdmin):
    list_display = ("tip_id", "title", "author", "created_at")
    list_select_related = ("author",)
    search_fields = ("title", "content")
    list_per_page = 50

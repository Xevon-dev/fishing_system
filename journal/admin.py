from django.contrib import admin

from .models import Catches, FishingTripPhotos, FishingTrips, TipLike, Tips


@admin.register(FishingTrips)
class FishingTripsAdmin(admin.ModelAdmin):
    list_display = ("trip_id", "user", "water_body", "created_at", "updated_at", "type", "method")
    list_select_related = ("user", "water_body", "type", "method")
    list_filter = ("type", "method")
    search_fields = ("water_body__name", "note", "bait_note", "method_note")
    exclude = ("start_time", "end_time", "hours_spent")
    list_per_page = 50


@admin.register(Catches)
class CatchesAdmin(admin.ModelAdmin):
    list_display = ("catch_id", "trip", "fish", "weight_kg", "quantity", "tackle")
    list_select_related = ("trip", "fish", "tackle")
    list_filter = ("fish", "tackle")
    search_fields = ("custom_fish_name", "trip__water_body__name", "bait_note")
    list_per_page = 50


@admin.register(Tips)
class TipsAdmin(admin.ModelAdmin):
    list_display = ("tip_id", "title", "author", "created_at")
    list_select_related = ("author",)
    search_fields = ("title", "content")
    list_per_page = 50


@admin.register(FishingTripPhotos)
class FishingTripPhotosAdmin(admin.ModelAdmin):
    list_display = ("photo_id", "trip", "photo")
    list_select_related = ("trip",)
    search_fields = ("trip__water_body__name", "trip__user__username")


@admin.register(TipLike)
class TipLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "tip", "user", "is_like", "created_at")
    list_select_related = ("tip", "user")
    list_filter = ("is_like", "created_at")
    search_fields = ("tip__title", "user__username")

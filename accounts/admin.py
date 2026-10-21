from django.contrib import admin

from .models import Levels, Users


@admin.register(Levels)
class LevelsAdmin(admin.ModelAdmin):
    list_display = ("level_id", "name")
    search_fields = ("name",)


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "email", "level", "created_at")
    list_select_related = ("level",)
    list_filter = ("level",)
    search_fields = ("username", "email")
    exclude = ("password_hash",)

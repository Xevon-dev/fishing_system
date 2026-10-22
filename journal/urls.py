from django.urls import path

from .views import (
    add_tip_view,
    add_trip_view,
    delete_trip_view,
    edit_tip_view,
    edit_trip_view,
    journal_view,
    stats_view,
    tips_list_view,
)

urlpatterns = [
    path("tips/", tips_list_view, name="tips_list"),
    path("tips/add/", add_tip_view, name="add_tip"),
    path("tips/<int:tip_id>/edit/", edit_tip_view, name="edit_tip"),
    path("journal/", journal_view, name="journal"),
    path("journal/add/", add_trip_view, name="add_trip"),
    path("journal/<int:trip_id>/edit/", edit_trip_view, name="edit_trip"),
    path("journal/<int:trip_id>/delete/", delete_trip_view, name="delete_trip"),
    path("stats/", stats_view, name="stats"),
]

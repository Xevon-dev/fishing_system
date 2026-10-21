from django.urls import path

from . import stats, tips, trips

urlpatterns = [
    path("tips/", tips.tips_list_view, name="tips_list"),
    path("tips/add/", tips.add_tip_view, name="add_tip"),
    path("journal/", trips.journal_view, name="journal"),
    path("journal/add/", trips.add_trip_view, name="add_trip"),
    path("journal/<int:trip_id>/edit/", trips.edit_trip_view, name="edit_trip"),
    path("journal/<int:trip_id>/delete/", trips.delete_trip_view, name="delete_trip"),
    path("stats/", stats.stats_view, name="stats"),
]

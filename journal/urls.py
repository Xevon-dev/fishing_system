from django.urls import path
from . import views

urlpatterns = [
    path("tips/", views.tips_list_view, name="tips_list"),
    path("journal/", views.journal_view, name="journal"),
    path("stats/", views.stats_view, name="stats"),
    path("tips/add/", views.add_tip_view, name="add_tip"),
]

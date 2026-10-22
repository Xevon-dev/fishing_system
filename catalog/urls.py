from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("map/", views.water_bodies_view, name="water_bodies"),
    path("map/<slug:region>/geojson/", views.water_bodies_geojson, name="water_bodies_geojson"),
    path("map/water/<int:water_body_id>/geojson/", views.water_body_geojson, name="water_body_geojson"),
    path("map/weather/", views.weather_view, name="weather"),
    path("map/advice/", views.advice_view, name="advice"),
    path("fish/", views.fish_advice_view, name="fish_advice"),
    path("methods/", views.methods_view, name="methods"),
    path("tackle/", views.tackle_view, name="tackle"),
    path("tackle/<int:fish_id>/", views.tackle_view, name="tackle_fish"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("map/", views.water_bodies_view, name="water_bodies"),
    path("map/<slug:region>/geojson/", views.water_bodies_geojson, name="water_bodies_geojson"),
    path("map/weather/", views.weather_view, name="weather"),
    path("fish/", views.fish_advice_view, name="fish_advice"),
    path("tackle/", views.tackle_view, name="tackle"),
    path("methods/", views.methods_view, name="methods"),
]

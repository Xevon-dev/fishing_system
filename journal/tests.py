import unittest

from django.contrib import admin
from django.urls import resolve, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.models import Levels, TestAnswers, TestQuestions, Users
from catalog.models import (
    FishCategory,
    FishSpecies,
    FishingMethods,
    FishingTypes,
    Tackle,
    TackleSets,
    WaterBodies,
)
from .forms import GenericFishingTripForm
from .models import Catches, FishingTripPhotos, FishingTrips, TipLike, Tips
from .views.generic_trips import (
    FishingTripCreateView,
    FishingTripDeleteView,
    FishingTripDetailView,
    FishingTripListView,
    FishingTripUpdateView,
    SessionOwnerRequiredMixin,
)
from .views.tips import TipsDetailView, TipsListView


class GenericViewRouteTests(unittest.TestCase):
    def test_trip_list_is_paginated_and_model_has_canonical_url(self):
        self.assertEqual(FishingTripListView.paginate_by, 20)
        trip = FishingTrips(trip_id=37)
        self.assertEqual(
            trip.get_absolute_url(),
            reverse("trip_record_detail", kwargs={"pk": 37}),
        )

    def test_session_owner_mixin_uses_django_login_required_mixin(self):
        self.assertTrue(issubclass(SessionOwnerRequiredMixin, LoginRequiredMixin))

    def test_fishing_trip_crud_routes_use_generic_views(self):
        expected = {
            "trip_records": (FishingTripListView, ListView),
            "trip_record_add": (FishingTripCreateView, CreateView),
            "trip_record_detail": (FishingTripDetailView, DetailView),
            "trip_record_edit": (FishingTripUpdateView, UpdateView),
            "trip_record_delete": (FishingTripDeleteView, DeleteView),
        }

        for route_name, (view_class, generic_class) in expected.items():
            with self.subTest(route=route_name):
                path = reverse(route_name, kwargs={"pk": 1}) if route_name in {
                    "trip_record_detail", "trip_record_edit", "trip_record_delete"
                } else reverse(route_name)
                self.assertIs(resolve(path).func.view_class, view_class)
                self.assertTrue(issubclass(view_class, generic_class))

    def test_trip_model_form_excludes_owner(self):
        self.assertEqual(
            tuple(GenericFishingTripForm._meta.fields),
            ("water_body", "type", "method_note", "note"),
        )

    def test_tips_have_generic_list_and_detail_views(self):
        self.assertTrue(issubclass(TipsListView, ListView))
        self.assertTrue(issubclass(TipsDetailView, DetailView))
        self.assertIs(resolve(reverse("tips_list")).func.view_class, TipsListView)


class ModelAdminRegistrationTests(unittest.TestCase):
    def test_each_project_model_has_a_configured_admin(self):
        models = (
            Levels, Users, TestQuestions, TestAnswers,
            WaterBodies, FishSpecies, FishCategory, FishingTypes,
            FishingMethods, Tackle, TackleSets,
            FishingTrips, FishingTripPhotos, Catches, Tips, TipLike,
        )

        for model in models:
            with self.subTest(model=model.__name__):
                self.assertTrue(admin.site.is_registered(model))
                model_admin = admin.site._registry[model]
                self.assertTrue(model_admin.list_display)
                self.assertTrue(model_admin.search_fields or model_admin.list_filter)

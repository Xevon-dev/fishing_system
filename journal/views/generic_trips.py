from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ..common import current_user
from ..forms import GenericFishingTripForm
from ..models import Catches, FishingTrips


class SessionOwnerRequiredMixin(LoginRequiredMixin):
    login_url = "accounts:login"

    def dispatch(self, request, *args, **kwargs):
        self.owner = current_user(request)
        if not self.owner:
            return redirect("accounts:login")
        request.user = self.owner
        return super().dispatch(request, *args, **kwargs)


class FishingTripListView(SessionOwnerRequiredMixin, ListView):
    model = FishingTrips
    template_name = "journal/trip_list.html"
    context_object_name = "trips"
    paginate_by = 20

    def get_queryset(self):
        return (
            FishingTrips.objects.filter(user_id=self.owner.user_id)
            .select_related("water_body", "type", "method")
            .prefetch_related("photos", "catches_set__fish")
            .order_by("-created_at")
        )


class FishingTripDetailView(SessionOwnerRequiredMixin, DetailView):
    model = FishingTrips
    template_name = "journal/trip_detail.html"
    context_object_name = "trip"

    def get_queryset(self):
        return (
            FishingTrips.objects.filter(user_id=self.owner.user_id)
            .select_related("water_body", "type", "method")
            .prefetch_related("photos", "catches_set__fish", "catches_set__tackle")
        )


class FishingTripCreateView(SessionOwnerRequiredMixin, CreateView):
    model = FishingTrips
    form_class = GenericFishingTripForm
    template_name = "journal/trip_form.html"
    success_url = reverse_lazy("journal:trip_records")

    def form_valid(self, form):
        form.instance.user = self.owner
        form.instance.start_time = timezone.now()
        return super().form_valid(form)


class FishingTripUpdateView(SessionOwnerRequiredMixin, UpdateView):
    model = FishingTrips
    form_class = GenericFishingTripForm
    template_name = "journal/trip_form.html"
    success_url = reverse_lazy("journal:trip_records")

    def get_queryset(self):
        return FishingTrips.objects.filter(user_id=self.owner.user_id)

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)


class FishingTripDeleteView(SessionOwnerRequiredMixin, DeleteView):
    model = FishingTrips
    template_name = "journal/trip_confirm_delete.html"
    success_url = reverse_lazy("journal:trip_records")

    def get_queryset(self):
        return FishingTrips.objects.filter(user_id=self.owner.user_id).prefetch_related("photos")

    def form_valid(self, form):
        with transaction.atomic():
            for photo in self.object.photos.all():
                photo.photo.delete(save=False)
            Catches.objects.filter(trip_id=self.object.trip_id).delete()
            self.object.delete()
        return HttpResponseRedirect(self.get_success_url())



from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from journal.models import Catches, FishingTrips, Tips
from .session import current_user, logout_user


@require_POST
def delete_account_view(request):
    user = current_user(request)
    if not user:
        return redirect("login")

    trips = FishingTrips.objects.filter(user_id=user.user_id)
    Catches.objects.filter(trip__user_id=user.user_id).delete()
    trips.delete()
    Tips.objects.filter(author_id=user.user_id).delete()

    user.delete()
    logout_user(request)

    return redirect("home")

from django.urls import path

from . import fishing_test, login, profile, registration

urlpatterns = [
    path("register/", registration.register_view, name="register"),
    path("login/", login.login_view, name="login"),
    path("logout/", login.logout_view, name="logout"),
    path("profile/", profile.profile_view, name="profile"),
    path("fishing-test/", fishing_test.fishing_test_view, name="fishing_test"),
]

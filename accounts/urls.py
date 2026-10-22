from django.urls import path

from .views import (
    delete_account_view,
    fishing_test_view,
    login_view,
    logout_view,
    password_view,
    profile_view,
    register_view,
    username_view,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/password/", password_view, name="password"),
    path("profile/name/", username_view, name="username"),
    path("profile/delete/", delete_account_view, name="delete_account"),
    path("fishing-test/", fishing_test_view, name="fishing_test"),
]

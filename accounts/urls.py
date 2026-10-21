from django.urls import path

from . import (
    delete_account,
    fishing_test,
    login,
    password,
    profile,
    registration,
    username,
)

urlpatterns = [
    path("register/", registration.register_view, name="register"),
    path("login/", login.login_view, name="login"),
    path("logout/", login.logout_view, name="logout"),
    path("profile/", profile.profile_view, name="profile"),
    path("profile/password/", password.password_view, name="password"),
    path("profile/name/", username.username_view, name="username"),
    path("profile/delete/", delete_account.delete_account_view, name="delete_account"),
    path("fishing-test/", fishing_test.fishing_test_view, name="fishing_test"),
]

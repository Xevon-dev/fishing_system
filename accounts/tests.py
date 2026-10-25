import unittest

from django.test import RequestFactory

from .forms import RegistrationForm
from .views.login import logout_view
from .views.registration import register_view


class LogoutViewTests(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_is_not_allowed(self):
        request = self.factory.get("/accounts/logout/")

        response = logout_view(request)

        self.assertEqual(response.status_code, 405)

    def test_post_clears_session_and_redirects_home(self):
        request = self.factory.post("/accounts/logout/")
        request.session = {"user_id": 42}

        response = logout_view(request)

        self.assertNotIn("user_id", request.session)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")


class RegistrationFormTests(unittest.TestCase):
    def test_registration_form_uses_django_user_creation_form_fields(self):
        form = RegistrationForm()

        self.assertEqual(
            set(form.fields),
            {"username", "email", "password1", "password2", "fishing_level"},
        )

    def test_registration_page_renders(self):
        request = RequestFactory().get("/accounts/register/")
        request.session = {}

        response = register_view(request)

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('name="password1"', content)
        self.assertIn('name="password2"', content)

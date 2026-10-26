from django.test import TestCase

from django.urls import reverse

from .models import FishSpecies


class FishEncyclopediaTests(TestCase):
    def test_encyclopedia_is_available_to_anonymous_users(self):
        response = self.client.get(reverse("catalog:fish_advice"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Енциклопедія рибака")

    def test_shows_fish_without_fishing_type_and_offers_season_info_link(self):
        FishSpecies.objects.create(name="Щука")

        response = self.client.get(reverse("catalog:fish_advice"))

        self.assertContains(response, "Щука")
        self.assertContains(response, "Коли ловити та нерест")
        self.assertContains(
            response,
            "%D0%A9%D1%83%D0%BA%D0%B0+%D0%BA%D0%BE%D0%BB%D0%B8+%D0%BB%D0%BE%D0%B2%D0%B8%D1%82%D0%B8+%D0%BD%D0%B5%D1%80%D0%B5%D1%81%D1%82",
        )

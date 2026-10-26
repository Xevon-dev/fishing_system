from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Levels, Users
from catalog.models import FishSpecies, FishingTypes, WaterBodies
from journal.models import Catches, FishingTrips, Tips


DEMO_USERNAME = "demo_fisher"
DEMO_EMAIL = "demo-fisher@example.invalid"
DEMO_PASSWORD = "DemoFish123"


class Command(BaseCommand):
    help = "Створює невеликий набір вигаданих даних для демонстрації проєкту."

    def handle(self, *args, **options):
        level = Levels.objects.filter(name="Початківець").first()
        if level is None:
            level = Levels.objects.create(name="Початківець")

        user = Users.objects.filter(email=DEMO_EMAIL).first()
        if user is None:
            user = Users.objects.create(
                username=DEMO_USERNAME,
                email=DEMO_EMAIL,
                password_hash=make_password(DEMO_PASSWORD),
                level=level,
                created_at=timezone.now(),
            )
        else:
            user.level = level
            user.password_hash = make_password(DEMO_PASSWORD)
            user.save(update_fields=("level", "password_hash"))

        water_bodies = [
            self._get_or_create(WaterBodies, {"name": "Демо-озеро"}, {
                "type": "Озеро",
                "region": "Демо-регіон",
                "description": "Вигадана водойма для демонстрації журналу.",
            }),
            self._get_or_create(WaterBodies, {"name": "Демо-річка"}, {
                "type": "Річка",
                "region": "Демо-регіон",
                "description": "Вигадана водойма для демонстрації журналу.",
            }),
        ]
        fish = [
            self._get_or_create(FishSpecies, {"name": "Демо-короп"}, {
                "description": "Вигаданий вид для демонстраційних записів.",
                "advice": "",
                "wikipedia": "",
                "image_source": "",
            }),
            self._get_or_create(FishSpecies, {"name": "Демо-окунь"}, {
                "description": "Вигаданий вид для демонстраційних записів.",
                "advice": "",
                "wikipedia": "",
                "image_source": "",
            }),
        ]
        types = [
            self._get_or_create(FishingTypes, {"name": "Демо-поплавцева ловля"}, {
                "description": "Демонстраційний тип риболовлі.",
                "video_url": "",
            }),
            self._get_or_create(FishingTypes, {"name": "Демо-спінінг"}, {
                "description": "Демонстраційний тип риболовлі.",
                "video_url": "",
            }),
        ]
        for fishing_type, species in zip(types, fish):
            fishing_type.fish.add(species)

        trip_specs = (
            ("Демо-сесія на озері", water_bodies[0], types[0], timezone.now() - timedelta(days=7)),
            ("Демо-сесія на річці", water_bodies[1], types[1], timezone.now() - timedelta(days=2)),
        )
        trips = []
        for note, water_body, fishing_type, started_at in trip_specs:
            trip = FishingTrips.objects.filter(user=user, note=note).first()
            if trip is None:
                trip = FishingTrips.objects.create(
                    user=user,
                    water_body=water_body,
                    type=fishing_type,
                    start_time=started_at,
                    note=note,
                )
            trips.append(trip)

        self._get_or_create(Catches, {
            "trip": trips[0], "fish": fish[0], "custom_fish_name": "",
        }, {
            "weight_kg": Decimal("2.40"),
            "quantity": 1,
        })
        self._get_or_create(Catches, {
            "trip": trips[1], "fish": fish[1], "custom_fish_name": "",
        }, {
            "weight_kg": Decimal("0.65"),
            "quantity": 2,
        })

        tip_title = "Демо-порада для риболовлі"
        tip = Tips.objects.filter(author=user, title=tip_title).first()
        if tip is None:
            tip = Tips.objects.create(
                author=user,
                title=tip_title,
                fish=fish[0],
                applies_to_all_fish=False,
                content="Це вигадана порада, додана лише для демонстрації роботи сайту.",
                created_at=timezone.now(),
            )
            tip.fishes.set([fish[0]])

        self.stdout.write(self.style.SUCCESS("Демо-дані готові."))
        self.stdout.write(f"Логін: {DEMO_USERNAME}")
        self.stdout.write(f"Пароль: {DEMO_PASSWORD}")

    @staticmethod
    def _get_or_create(model, lookup, defaults):
        instance = model.objects.filter(**lookup).first()
        if instance is None:
            instance = model.objects.create(**lookup, **defaults)
        return instance

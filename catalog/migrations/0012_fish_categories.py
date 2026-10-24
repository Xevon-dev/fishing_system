from django.db import migrations, models
import django.db.models.deletion


CATEGORIES = {
    "peaceful": {
        "name": "Мирна риба",
        "fish": (
            "Короп", "Карась", "Лящ", "Плітка", "Линь", "Товстолобик",
            "Білий амур", "Плотва", "Краснопірка", "В'юн", "Уклейка", "Піскар",
        ),
    },
    "predatory": {
        "name": "Хижа риба",
        "fish": ("Окунь", "Щука", "Судак", "Сом", "Голавль", "Жерех", "Язь"),
    },
    "coldwater-salmonids": {
        "name": "Холодноводні й лососеві",
        "fish": ("Форель", "Харіус", "Піскар"),
    },
    "rare": {
        "name": "Червона книга / рідкісні",
        "fish": ("Харіус",),
    },
}


def populate_categories(apps, schema_editor):
    FishSpecies = apps.get_model("catalog", "FishSpecies")
    FishCategory = apps.get_model("catalog", "FishCategory")

    for slug, data in CATEGORIES.items():
        category, _ = FishCategory.objects.get_or_create(
            slug=slug,
            defaults={"name": data["name"]},
        )
        for fish_name in data["fish"]:
            fish = FishSpecies.objects.filter(name=fish_name).first()
            if fish:
                fish.categories.add(category)


class Migration(migrations.Migration):
    dependencies = [("catalog", "0011_fill_fishing_type_descriptions")]

    operations = [
        migrations.CreateModel(
            name="FishCategory",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=100, unique=True)),
            ],
            options={"db_table": "fish_categories", "ordering": ("id",)},
        ),
        migrations.AddField(
            model_name="fishspecies",
            name="categories",
            field=models.ManyToManyField(blank=True, related_name="fish", to="catalog.fishcategory"),
        ),
        migrations.RunPython(populate_categories, migrations.RunPython.noop),
    ]

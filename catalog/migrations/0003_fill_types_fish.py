from django.db import migrations

FISH_BY_TYPE = {
    "Карпова": ("Короп", "Сазан", "Білий амур", "Товстолобик", "Карась"),
    "Фідерна": ("Лящ", "Карась", "Плітка", "Короп", "Плотва"),
    "Спінінгова": ("Щука", "Окунь", "Судак", "Жерех", "Сом", "Голавль"),
    "Поплавкова": ("Плітка", "Плотва", "Краснопірка", "Уклейка", "Линь", "Язь", "Пескарь"),
    "Донна": ("Сом", "Короп", "Сазан", "В'юн"),
    "Зимова": ("Окунь", "Щука", "Судак", "Плотва", "Лящ"),
    "З човна": ("Сом", "Судак", "Щука"),
    "Нахлист": ("Форель", "Харіус", "Голавль", "Язь"),
}


def fill_types_fish(apps, schema_editor):
    FishingTypes = apps.get_model("catalog", "FishingTypes")
    FishSpecies = apps.get_model("catalog", "FishSpecies")

    for type_name, fish_names in FISH_BY_TYPE.items():
        fishing_type = FishingTypes.objects.filter(name=type_name).first()
        if not fishing_type:
            continue

        for fish_name in fish_names:
            fish = FishSpecies.objects.filter(name=fish_name).first()
            if fish:
                fishing_type.fish.add(fish)


def clear_types_fish(apps, schema_editor):
    FishingTypes = apps.get_model("catalog", "FishingTypes")

    for fishing_type in FishingTypes.objects.all():
        fishing_type.fish.clear()


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_fishingtypes_fish"),
    ]

    operations = [
        migrations.RunPython(fill_types_fish, clear_types_fish),
    ]

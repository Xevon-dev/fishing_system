from django.db import migrations


TYPE_DESCRIPTIONS = {
    "Карпова": "Цілеспрямована ловля коропа й сазана: бойли, методні годівниці та довгі сесії біля перспективних місць.",
    "Фідерна": "Донна ловля з годівницею, яка доставляє прикорм у точку та допомагає утримувати рибу на місці.",
    "Спінінгова": "Активний пошук хижої риби за допомогою штучних приманок: воблерів, блешень і силікону.",
    "Поплавкова": "Ловля на вудку з поплавцем, що показує клювання; підходить для риболовлі біля берега та на різних глибинах.",
    "Донна": "Ловля з оснащенням, яке лежить на дні; дає змогу обловлювати глибокі ділянки та чекати на велику рибу.",
    "Зимова": "Ловля з льоду на зимові вудки, мормишки та блешні з пошуком риби на різних глибинах.",
    "З човна": "Риболовля з човна, що відкриває доступ до глибоких місць, руслових бровок і ділянок далеко від берега.",
    "Нахлист": "Ловля на штучну мушку легкою снастю; дає змогу точно подавати приманку на течії та мілководді.",
}


def fill_descriptions(apps, schema_editor):
    FishingTypes = apps.get_model("catalog", "FishingTypes")
    for name, description in TYPE_DESCRIPTIONS.items():
        FishingTypes.objects.filter(name=name, description__in=(None, "")).update(
            description=description
        )


class Migration(migrations.Migration):
    dependencies = [("catalog", "0010_fishspecies_image_source")]

    operations = [migrations.RunPython(fill_descriptions, migrations.RunPython.noop)]

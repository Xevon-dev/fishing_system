import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("journal", "0011_remove_fishingtrips_photo_fishingtripphotos"),
    ]

    operations = [
        migrations.CreateModel(
            name="TipLike",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("tip", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="journal.tips")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tip_likes", to="accounts.users")),
            ],
            options={"db_table": "tip_likes"},
        ),
        migrations.AddConstraint(
            model_name="tiplike",
            constraint=models.UniqueConstraint(fields=("tip", "user"), name="unique_tip_like_per_user"),
        ),
    ]

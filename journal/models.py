from django.db import models

# Create your models here.

class FishingTrips(models.Model):
    trip_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.Users', models.DO_NOTHING)
    water_body = models.ForeignKey('catalog.WaterBodies', models.DO_NOTHING)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    hours_spent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    note = models.TextField(blank=True, null=True)
    type = models.ForeignKey(
        'catalog.FishingTypes',
        models.DO_NOTHING,
        blank=True,
        null=True,
    )
    method = models.ForeignKey(
        'catalog.FishingMethods',
        models.DO_NOTHING,
        blank=True,
        null=True,
    )
    method_note = models.CharField(max_length=255, blank=True, null=True)
    bait_note = models.TextField(blank=True, null=True)
    fish_note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'fishing_trips'


class Catches(models.Model):
    catch_id = models.AutoField(primary_key=True)
    trip = models.ForeignKey('FishingTrips', models.DO_NOTHING)
    fish = models.ForeignKey('catalog.FishSpecies', models.DO_NOTHING)
    tackle = models.ForeignKey(
        'catalog.Tackle',
        models.DO_NOTHING,
        blank=True,
        null=True
    )
    weight_kg = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )
    quantity = models.IntegerField(blank=True, null=True)
    photo_url = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'catches'


class Tips(models.Model):
    tip_id = models.AutoField(primary_key=True)
    author = models.ForeignKey('accounts.Users', models.DO_NOTHING)
    title = models.CharField(max_length=200)
    fish = models.ForeignKey(
        'catalog.FishSpecies',
        models.DO_NOTHING,
        blank=True,
        null=True
    )
    content = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tips'
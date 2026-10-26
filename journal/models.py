from django.db import models
from django.urls import reverse

# Create your models here.

class FishingTrips(models.Model):
    trip_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
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

    class Meta:
        db_table = 'fishing_trips'

    def get_absolute_url(self):
        return reverse("trip_record_detail", kwargs={"pk": self.pk})


class FishingTripPhotos(models.Model):
    photo_id = models.AutoField(primary_key=True)
    trip = models.ForeignKey(
        'FishingTrips',
        models.CASCADE,
        related_name='photos',
    )
    photo = models.ImageField(upload_to="trips/")

    class Meta:
        db_table = "fishing_trip_photos"


class Catches(models.Model):
    catch_id = models.AutoField(primary_key=True)
    caught_at = models.DateTimeField(blank=True, null=True)
    trip = models.ForeignKey('FishingTrips', models.DO_NOTHING)
    fish = models.ForeignKey(
        'catalog.FishSpecies', models.DO_NOTHING, blank=True, null=True
    )
    custom_fish_name = models.CharField(max_length=100, blank=True, default="")
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
    tackle_note = models.CharField(max_length=200, blank=True, default="")
    bait_note = models.TextField(blank=True, default="")
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
    fishes = models.ManyToManyField(
        'catalog.FishSpecies',
        related_name='multi_tips',
        blank=True,
    )
    applies_to_all_fish = models.BooleanField(default=False)
    content = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to="tips/", blank=True, null=True)

    class Meta:
        db_table = 'tips'


class TipLike(models.Model):
    id = models.AutoField(primary_key=True)
    tip = models.ForeignKey(Tips, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE, related_name="tip_likes")
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tip_likes"
        constraints = [
            models.UniqueConstraint(fields=("tip", "user"), name="unique_tip_like_per_user"),
        ]

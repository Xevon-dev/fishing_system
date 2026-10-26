import re

from django.db import models

# Create your models here.


class WaterBodies(models.Model):
    water_body_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=45, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    region_slug = models.CharField(max_length=50, blank=True, default="")
    area_km2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    depth = models.CharField(max_length=100, blank=True, null=True)
    fish_list = models.CharField(max_length=255, blank=True, null=True)
    wikipedia = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    geometry = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'water_bodies'

    def __str__(self):
        return self.name


class FishSpecies(models.Model):
    fish_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="fish/", blank=True)
    wikipedia = models.URLField(max_length=500, blank=True)
    image_source = models.URLField(max_length=500, blank=True)
    categories = models.ManyToManyField(
        "FishCategory",
        related_name="fish",
        blank=True,
    )

    class Meta:
        db_table = 'fish_species'

    def __str__(self):
        return self.name


class FishCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        db_table = "fish_categories"
        ordering = ("id",)

    def __str__(self):
        return self.name


class FishingTypes(models.Model):
    type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    fish = models.ManyToManyField(
        'FishSpecies',
        db_table='fishing_types_fish',
        blank=True,
    )
    video_url = models.URLField(blank=True)

    class Meta:
        db_table = 'fishing_types'

    def __str__(self):
        return self.name

    @property
    def video_id(self):
        match = re.search(r'(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})', self.video_url)
        return match.group(1) if match else ''


class FishingMethods(models.Model):
    method_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True)
    min_level = models.ForeignKey('accounts.Levels', models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey('FishingTypes', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'fishing_methods'

    def __str__(self):
        return self.name

    @property
    def video_id(self):
        match = re.search(r'(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})', self.video_url)
        return match.group(1) if match else ''


class Tackle(models.Model):
    tackle_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    kind = models.CharField(max_length=45, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0)
    tier = models.CharField(max_length=20, blank=True)
    url = models.URLField(max_length=300, blank=True)
    image = models.URLField(max_length=300, blank=True)
    shop = models.CharField(max_length=50, blank=True, default='Flagman')
    type = models.ForeignKey('FishingTypes', models.DO_NOTHING, blank=True, null=True)
    fish = models.ManyToManyField('FishSpecies', db_table='tackle_fish', blank=True)

    class Meta:
        db_table = 'tackle'

    def __str__(self):
        return self.name


class TackleSets(models.Model):
    set_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    tier = models.CharField(max_length=20, blank=True)
    url = models.URLField(max_length=300, blank=True)
    image = models.URLField(max_length=300, blank=True)
    shop = models.CharField(max_length=50, blank=True, default='Flagman')
    type = models.ForeignKey('FishingTypes', models.DO_NOTHING, blank=True, null=True)
    fish = models.ManyToManyField('FishSpecies', db_table='tackle_sets_fish', blank=True)

    class Meta:
        db_table = 'tackle_sets'

    def __str__(self):
        return self.name

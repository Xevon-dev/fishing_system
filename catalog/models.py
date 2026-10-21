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
        managed = False
        db_table = 'water_bodies'


class FishSpecies(models.Model):
    fish_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fish_species'


class WaterBodyFish(models.Model):
    water_body_fish_id = models.AutoField(primary_key=True)
    water_body = models.ForeignKey('WaterBodies', models.DO_NOTHING)
    fish = models.ForeignKey('FishSpecies', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'water_body_fish'
        unique_together = (('water_body', 'fish'),)


class FishingTypes(models.Model):
    type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishing_types'


class FishingMethods(models.Model):
    method_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    min_level = models.ForeignKey('accounts.Levels', models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey('FishingTypes', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishing_methods'


class Tackle(models.Model):
    tackle_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=45, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tackle'


class TackleRecommendations(models.Model):
    rec_id = models.AutoField(primary_key=True)
    fish = models.ForeignKey('FishSpecies', models.DO_NOTHING)
    tackle = models.ForeignKey('Tackle', models.DO_NOTHING)
    method = models.ForeignKey('FishingMethods', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tackle_recommendations'
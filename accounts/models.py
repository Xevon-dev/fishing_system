from django.db import models

# Create your models here.

class Levels(models.Model):
    level_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'levels'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=100)
    password_hash = models.CharField(max_length=255)
    level = models.ForeignKey('Levels', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class LevelTests(models.Model):
    test_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    score = models.IntegerField(blank=True, null=True)
    suggested_level = models.ForeignKey('Levels', models.DO_NOTHING, blank=True, null=True)
    taken_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'level_tests'

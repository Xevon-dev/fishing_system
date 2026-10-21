from django.db import models

# Create your models here.

class Levels(models.Model):
    level_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'levels'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=100)
    password_hash = models.CharField(max_length=255)
    level = models.ForeignKey('Levels', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'users'

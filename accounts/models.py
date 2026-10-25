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
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)

    class Meta:
        db_table = 'users'

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_beginner(self):
        return bool(self.level and self.level.name == 'Початківець')


class TestQuestions(models.Model):
    question_id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)
    position = models.IntegerField(default=0)

    class Meta:
        db_table = 'test_questions'
        ordering = ('position', 'question_id')


class TestAnswers(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(
        'TestQuestions',
        models.CASCADE,
        related_name='answers',
    )
    text = models.CharField(max_length=255)
    points = models.IntegerField(default=1)
    position = models.IntegerField(default=0)

    class Meta:
        db_table = 'test_answers'
        ordering = ('position', 'answer_id')

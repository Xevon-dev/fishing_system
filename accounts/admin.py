from django.contrib import admin

from .models import Levels, TestAnswers, TestQuestions, Users


@admin.register(Levels)
class LevelsAdmin(admin.ModelAdmin):
    list_display = ("level_id", "name")
    search_fields = ("name",)


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "email", "level", "created_at")
    list_select_related = ("level",)
    list_filter = ("level",)
    search_fields = ("username", "email")
    exclude = ("password_hash",)


class TestAnswersInline(admin.TabularInline):
    model = TestAnswers
    extra = 1
    fields = ("position", "text", "points")


@admin.register(TestQuestions)
class TestQuestionsAdmin(admin.ModelAdmin):
    list_display = ("question_id", "text", "position")
    search_fields = ("text",)
    inlines = (TestAnswersInline,)


@admin.register(TestAnswers)
class TestAnswersAdmin(admin.ModelAdmin):
    list_display = ("answer_id", "question", "text", "points", "position")
    list_select_related = ("question",)
    list_filter = ("question",)
    search_fields = ("text", "question__text")

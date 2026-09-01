from django.contrib import admin

from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "created_at",
    )
    search_fields = (
        "question",
        "answer",
    )
    readonly_fields = (
        "answer",
        "created_at",
    )
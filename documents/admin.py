from django.contrib import admin
from django.utils.html import format_html

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "has_file",
        "content_length",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("content", "created_at")

    fieldsets = (
        ("Document", {
            "fields": ("title", "file"),
            "description": (
                "Upload a .docx file. Its text is extracted automatically "
                "and indexed into the vector store on save."
            ),
        }),
        ("Extracted content", {
            "fields": ("content", "created_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="File", boolean=True)
    def has_file(self, obj):
        return bool(obj.file)

    @admin.display(description="Characters")
    def content_length(self, obj):
        return len(obj.content or "")
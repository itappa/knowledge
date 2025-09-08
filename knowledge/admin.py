from django.contrib import admin
from .models import Knowledge


@admin.register(Knowledge)
class KnowledgeAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "author",
        "is_public",
        "view_count",
        "updated_at",
    ]
    list_filter = ["category", "author", "is_public", "created_at"]
    search_fields = ["title", "content", "tags"]
    readonly_fields = ["view_count", "created_at", "updated_at"]

    fieldsets = (
        ("基本情報", {"fields": ("title", "content", "category", "tags")}),
        ("管理情報", {"fields": ("author", "is_public", "view_count")}),
        ("関連情報", {"fields": ("related_inquiries",), "classes": ("collapse",)}),
        (
            "日時情報",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

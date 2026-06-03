from django.contrib import admin

from .models import Client, Deal, Lead, Note, Task


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "phone", "source", "is_active", "created_at")
    search_fields = ("name", "company", "email", "phone")
    list_filter = ("is_active", "source", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "status",
        "priority",
        "estimated_budget",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "description", "client__name", "client__company")
    list_filter = ("status", "priority", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("client",)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("title", "lead", "value", "status", "expected_close_date", "created_at")
    search_fields = ("title", "lead__title", "lead__client__name", "lead__client__company")
    list_filter = ("status", "expected_close_date", "created_at")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("lead",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "lead", "status", "due_date", "created_at")
    search_fields = ("title", "description", "lead__title", "lead__client__name")
    list_filter = ("status", "due_date", "created_at")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("lead",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("lead", "created_at", "short_text")
    search_fields = ("text", "lead__title", "lead__client__name")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    autocomplete_fields = ("lead",)

    @admin.display(description="Text")
    def short_text(self, obj):
        return obj.text[:90]

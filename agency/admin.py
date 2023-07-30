from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from agency.models import Topic, Newspaper, Redactor


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ["title", "topic", "published_date"]
    search_fields = ["title"]
    list_filter = ["topic"]


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("years_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("years_of_experience",)}),
    )

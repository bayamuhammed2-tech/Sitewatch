from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "company",
        "location",
        "status",
        "progress",
        "start_date",
        "expected_completion_date",
    )

    list_filter = (
        "status",
        "company",
    )

    search_fields = (
        "name",
        "location",
        "company__company_name",
    )

    list_editable = (
        "status",
        "progress",
    )
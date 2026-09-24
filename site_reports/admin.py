from django.contrib import admin
from .models import DailySiteReport


@admin.register(DailySiteReport)
class DailySiteReportAdmin(admin.ModelAdmin):

    list_display = (
        "project",
        "report_date",
        "submitted_by",
        "workers_on_site",
        "progress_update",
        "created_at",
    )

    list_filter = (
        "report_date",
        "project",
    )

    search_fields = (
        "project__name",
        "submitted_by__username",
        "work_completed",
        "issues",
    )

    ordering = (
        "-report_date",
    )
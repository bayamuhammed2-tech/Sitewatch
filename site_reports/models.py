from django.conf import settings
from django.db import models
from projects.models import Project


class DailySiteReport(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="daily_reports",
    )

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="submitted_site_reports",
    )

    report_date = models.DateField()

    work_completed = models.TextField()

    workers_on_site = models.PositiveIntegerField(default=0)

    issues = models.TextField(
        blank=True,
        help_text="Describe any problems, delays, safety concerns, or other issues."
    )

    materials_used = models.TextField(
        blank=True,
        help_text="Record important materials used during the day."
    )

    progress_update = models.PositiveIntegerField(
        default=0,
        help_text="Overall project progress percentage after this report."
    )

    additional_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name} - {self.report_date}"
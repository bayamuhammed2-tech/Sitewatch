from django.contrib import admin
from .models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "company",
        "project",
        "job_type",
        "location",
        "number_of_workers",
        "status",
        "application_deadline",
        "created_at",
    )

    list_filter = (
        "status",
        "job_type",
        "company",
    )

    search_fields = (
        "title",
        "location",
        "company__company_name",
        "project__name",
        "required_skills",
    )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "job",
        "worker",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "job__title",
        "worker__user__username",
    )

    list_editable = (
        "status",
    )
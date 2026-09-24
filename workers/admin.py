from django.contrib import admin
from .models import WorkerProfile


@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "location",
        "years_of_experience",
        "availability",
        "created_at",
    )

    list_filter = (
        "availability",
        "location",
    )

    search_fields = (
        "user__username",
        "location",
        "skills",
    )
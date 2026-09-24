from django.contrib import admin
from .models import WorkerAssignment, Attendance


@admin.register(WorkerAssignment)
class WorkerAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "worker",
        "project",
        "job",
        "status",
        "start_date",
        "end_date",
    )

    list_filter = (
        "status",
        "project",
    )

    search_fields = (
        "worker__user__username",
        "project__name",
        "job__title",
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "assignment",
        "date",
        "status",
        "check_in",
        "check_out",
    )

    list_filter = (
        "status",
        "date",
    )

    search_fields = (
        "assignment__worker__user__username",
        "assignment__project__name",
    )
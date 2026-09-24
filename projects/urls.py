from django.urls import path

from . import views


app_name = "projects"


urlpatterns = [

    path(
        "create/",
        views.create_project,
        name="create_project",
    ),

    path(
        "",
        views.project_list,
        name="project_list",
    ),

    path(
    "<int:project_id>/attendance/",
    views.attendance,
    name="attendance",
),

    path(
    "my-attendance/",
    views.worker_attendance,
    name="worker_attendance",
),



    path(
        "<int:project_id>/",
        views.project_detail,
        name="project_detail",
    ),

    path(
    "attendance/",
    views.attendance_projects,
    name="attendance_projects",
),

    path(
        "<int:project_id>/assign-worker/",
        views.assign_worker,
        name="assign_worker",
    ),

    path(
    "my-projects/",
    views.worker_projects,
    name="worker_projects",
),

path(
    "my-projects/<int:project_id>/",
    views.worker_project_detail,
    name="worker_project_detail",
),



    path(
        "<int:project_id>/attendance/",
        views.attendance,
        name="attendance",
    ),

    path(
        "<int:project_id>/attendance/<int:worker_id>/",
        views.mark_attendance,
        name="mark_attendance",
    ),
]
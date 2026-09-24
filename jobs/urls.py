from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("create/", views.create_job, name="create_job"),
    path("", views.job_list, name="job_list"),

    path(
        "applications/<int:application_id>/",
        views.application_detail,
        name="application_detail",
    ),

    path(
        "applications/<int:application_id>/status/<str:status>/",
        views.update_application_status,
        name="update_application_status",
    ),

    path("<int:job_id>/", views.job_detail, name="job_detail"),

    path(
        "<int:job_id>/apply/",
        views.apply_for_job,
        name="apply_for_job",
    ),
    path(
    "my-applications/",
    views.my_applications,
    name="my_applications",
    ),

    path(
    "applications/",
    views.application_list,
    name="application_list",
    )
]
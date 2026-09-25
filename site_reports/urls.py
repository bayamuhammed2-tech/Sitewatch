from django.urls import path

from . import views


app_name = "site_reports"


urlpatterns = [
    path("", views.report_list, name="report_list"),
    path("create/", views.create_report, name="create_report"),
    path("<int:report_id>/", views.report_detail, name="report_detail"),
]
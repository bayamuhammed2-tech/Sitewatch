from django.contrib import admin
from django.urls import path, include

from config import views as config_views
from accounts import views as account_views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),

    # Home page
    path("", config_views.home, name="home"),

    # Authentication
    path("register/", account_views.register, name="register"),
    path("login/", account_views.login_view, name="login"),
    path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html"
    ),
    name="password_reset",
),

path(
    "password-reset/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ),
    name="password_reset_done",
),

path(
    "password-reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"
    ),
    name="password_reset_confirm",
),

path(
    "password-reset/complete/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ),
    name="password_reset_complete",
),
    path("logout/", account_views.logout_view, name="logout"),

    # Dashboards
    path(
        "dashboard/",
        account_views.dashboard,
        name="dashboard",
    ),
    path(
        "dashboard/worker/",
        account_views.worker_dashboard,
        name="worker_dashboard",
    ),
    path(
        "dashboard/company/",
        account_views.company_dashboard,
        name="company_dashboard",
    ),

    # Apps
    path("companies/", include("companies.urls")),
    path("workers/", include("workers.urls")),
    path("jobs/", include("jobs.urls")),

    path(
    "notifications/",
    include("notifications.urls"),
    ),

    path(
    "projects/",
    include("projects.urls"),
    ),
]
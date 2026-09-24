from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from notifications.models import Notification

from .forms import UserRegistrationForm

from jobs.models import JobApplication
from workers.models import WorkerProfile


def register(request):
    """
    Handles user registration.
    If already logged in, redirects to dashboard.
    Upon successful registration, automatically logs the user in.
    """

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("dashboard")

    else:

        form = UserRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


def login_view(request):
    """
    Handles user login.
    """

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect("dashboard")

    else:

        form = AuthenticationForm()

    for field in form.fields.values():

        field.widget.attrs.update({
            "class": "form-input"
        })

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )


def logout_view(request):
    """
    Logs out the user and redirects them to login.
    """

    logout(request)

    return redirect("login")


@login_required
def dashboard(request):
    """
    Central dispatcher.
    Sends users to the correct dashboard based on role.
    """

    role = getattr(
        request.user,
        "role",
        None,
    )

    if role == "WORKER":

        return redirect(
            "worker_dashboard"
        )

    elif role == "COMPANY_ADMIN":

        return redirect(
            "company_dashboard"
        )

    return redirect("home")


@login_required
def worker_dashboard(request):

    if getattr(
        request.user,
        "role",
        None,
    ) != "WORKER":

        return redirect("dashboard")

    from notifications.models import Notification

    worker_profile, profile_created = (
        WorkerProfile.objects.get_or_create(
            user=request.user,
            defaults={
                "phone_number": "",
                "location": "",
                "skills": "",
                "years_of_experience": 0,
            },
        )
    )

    profile_complete = all([
        worker_profile.phone_number.strip(),
        worker_profile.location.strip(),
        worker_profile.skills.strip(),
    ])

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).count()

    return render(
        request,
        "accounts/worker_dashboard.html",
        {
            "unread_notifications": unread_notifications,
            "worker_profile": worker_profile,
            "profile_complete": profile_complete,
        },
    )
@login_required
def company_dashboard(request):

    if getattr(
        request.user,
        "role",
        None,
    ) != "COMPANY_ADMIN":
        return redirect("dashboard")

    from projects.models import Project, ProjectWorker
    from jobs.models import Job, JobApplication

    company = request.user.company

    # -----------------------------
    # PROJECTS
    # -----------------------------

    projects = Project.objects.filter(
        company=company
    ).order_by(
        "-created_at"
    )

    active_projects_count = projects.filter(
        status=Project.Status.ACTIVE
    ).count()

    total_projects_count = projects.count()

    # -----------------------------
    # WORKERS
    # -----------------------------

    registered_workers_count = ProjectWorker.objects.filter(
        project__company=company
    ).values(
        "worker_id"
    ).distinct().count()

    # -----------------------------
    # JOBS
    # -----------------------------

    open_jobs_count = Job.objects.filter(
        company=company,
        status=Job.Status.OPEN,
    ).count()

    total_jobs_count = Job.objects.filter(
        company=company
    ).count()

    # -----------------------------
    # APPLICATIONS
    # -----------------------------

    applications = JobApplication.objects.filter(
        job__company=company
    ).select_related(
        "job",
        "worker",
        "job__project",
    ).order_by(
        "-applied_at"
    )

    pending_applications = applications.filter(
        status=JobApplication.Status.PENDING
    )

    pending_applications_count = pending_applications.count()

    # -----------------------------
    # ASSIGNED WORKERS
    # -----------------------------

    assigned_workers = ProjectWorker.objects.filter(
        project__company=company
    ).select_related(
        "worker",
        "worker__user",
        "project",
    ).order_by(
        "-assigned_at"
    )

    assigned_workers_count = assigned_workers.values(
        "worker_id"
    ).distinct().count()

    # -----------------------------
    # RECENT PROJECTS
    # -----------------------------

    recent_projects = projects[:5]

    # -----------------------------
    # RECENT WORKERS
    # -----------------------------

    recent_workers = assigned_workers[:5]

    return render(
        request,
        "accounts/company_dashboard.html",
        {
            "company": company,

            # Projects
            "projects": projects,
            "recent_projects": recent_projects,
            "active_projects_count": active_projects_count,
            "total_projects_count": total_projects_count,

            # Workers
            "assigned_workers": assigned_workers,
            "recent_workers": recent_workers,
            "registered_workers_count": registered_workers_count,
            "assigned_workers_count": assigned_workers_count,

            # Jobs
            "open_jobs_count": open_jobs_count,
            "total_jobs_count": total_jobs_count,

            # Applications
            "applications": applications,
            "pending_applications": pending_applications,
            "pending_applications_count": pending_applications_count,
        },
    )
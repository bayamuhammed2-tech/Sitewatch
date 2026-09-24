from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from notifications.models import Notification

from .forms import JobForm, JobApplicationForm
from .models import Job, JobApplication
from companies.models import Company
from notifications.models import Notification

@login_required
def create_job(request):

    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    try:
        company = request.user.company
    except Company.DoesNotExist:
        return redirect("company_dashboard")

    if request.method == "POST":

        form = JobForm(
            request.POST,
            company=company
        )

        if form.is_valid():

            job = form.save(commit=False)

            job.company = company
            job.status = Job.Status.OPEN

            job.save()

            return redirect("company_dashboard")

    else:

        form = JobForm(company=company)

    return render(
        request,
        "jobs/create_job.html",
        {
            "form": form,
            "company": company,
        }
    )

@login_required
def job_list(request):

    if request.user.role != "WORKER":
        return redirect("dashboard")

    jobs = Job.objects.filter(
        status=Job.Status.OPEN
    ).select_related(
        "company",
        "project",
    ).order_by("-created_at")

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs,
        }
    )
@login_required
def job_detail(request, job_id):

    if request.user.role != "WORKER":
        return redirect("dashboard")

    job = Job.objects.select_related(
        "company",
        "project",
    ).get(
        id=job_id,
        status=Job.Status.OPEN,
    )

    worker = request.user.worker_profile

    already_applied = JobApplication.objects.filter(
        job=job,
        worker=worker,
    ).exists()

    return render(
        request,
        "jobs/job_detail.html",
        {
            "job": job,
            "already_applied": already_applied,
        }
    )
@login_required
def apply_for_job(request, job_id):

    if request.user.role != "WORKER":
        return redirect("dashboard")

    job = get_object_or_404(
        Job,
        id=job_id,
        status=Job.Status.OPEN,
    )

    worker = request.user.worker_profile

    if JobApplication.objects.filter(
        job=job,
        worker=worker,
    ).exists():
        return redirect(
            "jobs:job_detail",
            job_id=job.id
        )

    if request.method == "POST":

        form = JobApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(commit=False)

            application.job = job
            application.worker = worker

            application.save()

            # Create notification for the company
            Notification.objects.create(
                user=job.company.owner,
                notification_type=Notification.NotificationType.NEW_APPLICATION,
                title="New Job Application",
                message=(
                    f"{worker.user.get_full_name() or worker.user.username} "
                    f"has applied for the job '{job.title}'."
                ),
            )

            return redirect(
                "jobs:job_detail",
                job_id=job.id
            )

    else:
        form = JobApplicationForm()

    return render(
        request,
        "jobs/apply.html",
        {
            "job": job,
            "form": form,
        }
    )
@login_required
def application_detail(request, application_id):

    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    company = request.user.company

    application = get_object_or_404(
        JobApplication.objects.select_related(
            "job",
            "job__project",
            "worker",
            "worker__user",
        ),
        id=application_id,
        job__company=company,
    )

    return render(
        request,
        "jobs/application_detail.html",
        {
            "application": application,
        },
    )
@login_required
def update_application_status(request, application_id, status):

    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    if request.method != "POST":
        return redirect(
            "jobs:application_detail",
            application_id=application_id,
        )

    company = request.user.company

    application = get_object_or_404(
        JobApplication,
        id=application_id,
        job__company=company,
    )

    allowed_statuses = {
        JobApplication.Status.SHORTLISTED,
        JobApplication.Status.ACCEPTED,
        JobApplication.Status.REJECTED,
    }

    if status not in allowed_statuses:
        return redirect(
            "jobs:application_detail",
            application_id=application.id,
        )

    application.status = status
    application.save(
        update_fields=["status", "updated_at"]
    )

    status_messages = {
        JobApplication.Status.SHORTLISTED: (
            "Application shortlisted",
            f"Your application for {application.job.title} "
            "has been shortlisted by the company.",
        ),

        JobApplication.Status.ACCEPTED: (
            "Application accepted",
            f"Your application for {application.job.title} "
            "has been accepted by the company.",
        ),

        JobApplication.Status.REJECTED: (
            "Application update",
            f"Your application for {application.job.title} "
            "was not accepted by the company.",
        ),
    }

    title, message = status_messages[status]

    Notification.objects.create(
        user=application.worker.user,
        notification_type=Notification.NotificationType.APPLICATION_STATUS,
        title=title,
        message=message,
    )

    return redirect(
        "jobs:application_detail",
        application_id=application.id,
    )
@login_required
def my_applications(request):

    if request.user.role != "WORKER":
        return redirect("dashboard")

    worker = request.user.worker_profile

    applications = JobApplication.objects.filter(
        worker=worker
    ).select_related(
        "job",
        "job__company",
        "job__project",
    ).order_by("-applied_at")

    return render(
        request,
        "jobs/my_applications.html",
        {
            "applications": applications,
        },
    )

@login_required
def application_list(request):
    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    company = request.user.company

    applications = (
        JobApplication.objects
        .filter(job__company=company)
        .select_related(
            "job",
            "job__project",
            "worker",
            "worker__user",
        )
        .order_by("-applied_at")
    )

    return render(
        request,
        "jobs/application_list.html",
        {
            "applications": applications,
            "company": company,
        },
    )
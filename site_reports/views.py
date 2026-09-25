from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from companies.models import Company
from projects.models import Project
from .models import DailySiteReport


@login_required
def report_list(request):
    company = get_object_or_404(Company, owner=request.user)

    reports = (
        DailySiteReport.objects
        .filter(project__company=company)
        .select_related("project", "submitted_by")
        .order_by("-report_date", "-created_at")
    )

    return render(
        request,
        "site_reports/report_list.html",
        {
            "reports": reports,
            "company": company,
        },
    )


@login_required
def report_detail(request, report_id):
    company = get_object_or_404(Company, owner=request.user)

    report = get_object_or_404(
        DailySiteReport.objects.select_related(
            "project",
            "submitted_by",
        ),
        id=report_id,
        project__company=company,
    )

    return render(
        request,
        "site_reports/report_detail.html",
        {
            "report": report,
            "company": company,
        },
    )


@login_required
def create_report(request):
    company = get_object_or_404(Company, owner=request.user)

    projects = Project.objects.filter(company=company).order_by("name")

    if request.method == "POST":
        project_id = request.POST.get("project")
        report_date = request.POST.get("report_date")
        work_completed = request.POST.get("work_completed")
        workers_on_site = request.POST.get("workers_on_site") or 0
        issues = request.POST.get("issues", "")
        materials_used = request.POST.get("materials_used", "")
        progress_update = request.POST.get("progress_update") or 0
        additional_notes = request.POST.get("additional_notes", "")

        project = get_object_or_404(
            Project,
            id=project_id,
            company=company,
        )

        DailySiteReport.objects.create(
            project=project,
            submitted_by=request.user,
            report_date=report_date,
            work_completed=work_completed,
            workers_on_site=workers_on_site,
            issues=issues,
            materials_used=materials_used,
            progress_update=progress_update,
            additional_notes=additional_notes,
        )

        # Keep the project's progress synchronized with the latest report.
        project.progress = progress_update
        project.save(update_fields=["progress", "updated_at"])

        return redirect("site_reports:report_list")

    return render(
        request,
        "site_reports/create_report.html",
        {
            "projects": projects,
            "company": company,
        },
    )
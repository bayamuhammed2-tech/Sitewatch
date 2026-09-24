from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import ProjectForm, AttendanceForm
from .models import Project, ProjectWorker, Attendance

from jobs.models import JobApplication
from django.urls import reverse

@login_required
def create_project(request):

    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    company = request.user.company

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            project = form.save(commit=False)

            project.company = company

            project.save()

            return redirect(
                "projects:project_list"
            )

    else:
        form = ProjectForm()

    return render(
        request,
        "projects/create_project.html",
        {
            "form": form,
            "company": company,
        },
    )


@login_required
def project_list(request):

    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    company = request.user.company

    projects = Project.objects.filter(
        company=company
    ).order_by("-created_at")

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects,
        },
    )


@login_required
def project_detail(request, project_id):

    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    company = request.user.company

    project = get_object_or_404(
        Project,
        id=project_id,
        company=company,
    )

    assigned_workers = ProjectWorker.objects.filter(
        project=project
    ).select_related(
        "worker",
        "worker__user",
    )

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
            "assigned_workers": assigned_workers,
        },
    )


@login_required
def assign_worker(request, project_id):

    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    company = request.user.company

    project = get_object_or_404(
        Project,
        id=project_id,
        company=company,
    )

    accepted_applications = JobApplication.objects.filter(
        job__company=company,
        job__project=project,
        status=JobApplication.Status.ACCEPTED,
    ).select_related(
        "worker",
        "worker__user",
    )

    assigned_worker_ids = ProjectWorker.objects.filter(
        project=project
    ).values_list(
        "worker_id",
        flat=True,
    )

    available_applications = accepted_applications.exclude(
        worker_id__in=assigned_worker_ids
    )

    if request.method == "POST":

        worker_id = request.POST.get("worker_id")

        application = get_object_or_404(
            JobApplication,
            worker_id=worker_id,
            job__company=company,
            job__project=project,
            status=JobApplication.Status.ACCEPTED,
        )

        ProjectWorker.objects.get_or_create(
            project=project,
            worker=application.worker,
        )

        return redirect(
            "projects:project_detail",
            project_id=project.id,
        )

    return render(
        request,
        "projects/assign_worker.html",
        {
            "project": project,
            "available_applications": available_applications,
        },
    )

@login_required
def attendance(request, project_id):
    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    company = request.user.company

    project = get_object_or_404(
        Project,
        id=project_id,
        company=company,
    )

    assigned_workers = (
        ProjectWorker.objects
        .filter(project=project)
        .select_related("worker", "worker__user")
    )

    selected_date = request.GET.get("date")

    if selected_date:
        try:
            selected_date = timezone.datetime.strptime(
                selected_date,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            selected_date = timezone.localdate()
    else:
        selected_date = timezone.localdate()

    attendance_records = Attendance.objects.filter(
        project=project,
        date=selected_date,
    )

    attendance_by_worker = {
        record.worker_id: record
        for record in attendance_records
    }

    return render(
        request,
        "projects/attendance.html",
        {
            "project": project,
            "assigned_workers": assigned_workers,
            "attendance_records": attendance_by_worker,
            "selected_date": selected_date,
        },
    )

@login_required
def mark_attendance(request, project_id, worker_id):
    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    company = request.user.company

    project = get_object_or_404(
        Project,
        id=project_id,
        company=company,
    )

    project_worker = get_object_or_404(
        ProjectWorker,
        project=project,
        worker_id=worker_id,
    )

    selected_date = request.GET.get("date") or request.POST.get("date")

    if selected_date:
        try:
            selected_date = timezone.datetime.strptime(
                selected_date,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            selected_date = timezone.localdate()
    else:
        selected_date = timezone.localdate()

    if request.method == "POST":
        form = AttendanceForm(request.POST)

        if form.is_valid():
            Attendance.objects.update_or_create(
                project=project,
                worker=project_worker.worker,
                date=selected_date,
                defaults={
                    "status": form.cleaned_data["status"],
                    "notes": form.cleaned_data["notes"],
                },
            )

            return redirect(
                f"{reverse('projects:attendance', kwargs={'project_id': project.id})}"
                f"?date={selected_date:%Y-%m-%d}"
            )

    else:
        existing_record = Attendance.objects.filter(
            project=project,
            worker=project_worker.worker,
            date=selected_date,
        ).first()

        if existing_record:
            form = AttendanceForm(instance=existing_record)
        else:
            form = AttendanceForm()

    return render(
        request,
        "projects/mark_attendance.html",
        {
            "project": project,
            "project_worker": project_worker,
            "form": form,
            "selected_date": selected_date,
        },
    )
@login_required
def worker_projects(request):

    if request.user.role != "WORKER":
        return redirect("dashboard")

    worker = request.user.worker_profile

    assignments = ProjectWorker.objects.filter(
        worker=worker
    ).select_related(
        "project",
        "project__company",
    ).order_by(
        "-assigned_at"
    )

    return render(
        request,
        "projects/worker_projects.html",
        {
            "assignments": assignments,
        },
    )


@login_required
def worker_project_detail(request, project_id):

    if request.user.role != "WORKER":
        return redirect("dashboard")

    worker = request.user.worker_profile

    assignment = get_object_or_404(
        ProjectWorker.objects.select_related(
            "project",
            "project__company",
        ),
        project_id=project_id,
        worker=worker,
    )

    attendance_records = Attendance.objects.filter(
        project=assignment.project,
        worker=worker,
    ).order_by(
        "-date"
    )

    return render(
        request,
        "projects/worker_project_detail.html",
        {
            "project": assignment.project,
            "attendance_records": attendance_records,
        },
    )

@login_required
def worker_attendance(request):

    if request.user.role != "WORKER":
        return redirect("dashboard")

    worker = request.user.worker_profile

    attendance_records = Attendance.objects.filter(
        worker=worker
    ).select_related(
        "project",
        "project__company",
    ).order_by(
        "-date"
    )

    total_days = attendance_records.count()

    present_count = attendance_records.filter(
        status=Attendance.Status.PRESENT
    ).count()

    late_count = attendance_records.filter(
        status=Attendance.Status.LATE
    ).count()

    absent_count = attendance_records.filter(
        status=Attendance.Status.ABSENT
    ).count()

    attendance_rate = 0

    if total_days > 0:
        attendance_rate = round(
            (
                (present_count + late_count)
                / total_days
            ) * 100,
            1,
        )

    return render(
        request,
        "projects/worker_attendance.html",
        {
            "attendance_records": attendance_records,
            "total_days": total_days,
            "present_count": present_count,
            "late_count": late_count,
            "absent_count": absent_count,
            "attendance_rate": attendance_rate,
        },
    )

@login_required
def attendance_projects(request):

    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    company = request.user.company

    projects = Project.objects.filter(
        company=company
    ).order_by("-created_at")

    return render(
        request,
        "projects/attendance_projects.html",
        {
            "projects": projects,
        },
    )
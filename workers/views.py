from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import WorkerProfileForm
from .models import WorkerProfile


@login_required
def profile(request):
    if request.user.role != "WORKER":
        return redirect("dashboard")

    worker_profile, created = WorkerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "phone_number": "",
            "location": "",
            "skills": "",
            "years_of_experience": 0,
        },
    )

    if request.method == "POST":
        form = WorkerProfileForm(
            request.POST,
            instance=worker_profile,
        )

        if form.is_valid():
            form.save()
            return redirect("workers:profile")

    else:
        form = WorkerProfileForm(instance=worker_profile)

    return render(
        request,
        "workers/profile.html",
        {
            "form": form,
            "worker_profile": worker_profile,
        },
    )
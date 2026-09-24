from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from accounts.forms import UserRegistrationForm
from accounts.models import User
from workers.models import WorkerProfile
from companies.models import Company


def home(request):
    return render(request, "home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Create the correct profile based on account type
            if user.role == User.Role.WORKER:
                WorkerProfile.objects.create(
                    user=user,
                    phone_number="",
                    location="",
                    skills="",
                    years_of_experience=0,
                )

            elif user.role == User.Role.COMPANY:
                Company.objects.create(
                    owner=user,
                    company_name=user.username,
                    phone_number="",
                    email=user.email,
                    location="",
                )

            login(request, user)

            return redirect("dashboard")

    else:
        form = UserRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("dashboard")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form},
    )


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    role = getattr(request.user, "role", None)

    if role == User.Role.WORKER:
        return redirect("worker_dashboard")

    elif role == User.Role.COMPANY:
        return redirect("company_dashboard")

    return redirect("home")


@login_required
def worker_dashboard(request):
    if getattr(request.user, "role", None) != User.Role.WORKER:
        return redirect("dashboard")

    return render(
        request,
        "accounts/worker_dashboard.html",
    )


@login_required
def company_dashboard(request):
    if getattr(request.user, "role", None) != User.Role.COMPANY:
        return redirect("dashboard")

    return render(
        request,
        "accounts/company_dashboard.html",
    )
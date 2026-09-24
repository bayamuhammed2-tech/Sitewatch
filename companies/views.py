from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def company_profile(request):
    if request.user.role != "COMPANY_ADMIN":
        return redirect("dashboard")

    company = request.user.company

    return render(
        request,
        "companies/company_profile.html",
        {
            "company": company,
        },
    )
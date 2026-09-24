from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Notification


@login_required
def notification_list(request):

    if request.user.role not in ["WORKER", "COMPANY_ADMIN"]:
        return redirect("dashboard")

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).update(
        is_read=True
    )

    return render(
        request,
        "notifications/notifications.html",
        {
            "notifications": notifications,
        },
    )
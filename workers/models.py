from django.conf import settings
from django.db import models


class WorkerProfile(models.Model):
    class Availability(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        BUSY = "BUSY", "Busy"
        NOT_AVAILABLE = "NOT_AVAILABLE", "Not Available"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="worker_profile",
    )

    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)

    skills = models.TextField(
        help_text="List your construction skills."
    )

    years_of_experience = models.PositiveIntegerField(default=0)

    availability = models.CharField(
        max_length=20,
        choices=Availability.choices,
        default=Availability.AVAILABLE,
    )

    bio = models.TextField(
        blank=True,
        help_text="Tell employers a little about yourself."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
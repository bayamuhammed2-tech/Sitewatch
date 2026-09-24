from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        WORKER = "WORKER", "Worker"
        COMPANY = "COMPANY_ADMIN", "Company"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.WORKER,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Profile(models.Model):
    ROLE_CHOICES = [
        ("worker", "Worker"),
        ("company", "Company"),
    ]

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"
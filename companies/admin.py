from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "owner",
        "location",
        "verification_status",
        "created_at",
    )

    list_filter = (
        "verification_status",
        "location",
    )

    search_fields = (
        "company_name",
        "owner__username",
        "email",
        "location",
    )
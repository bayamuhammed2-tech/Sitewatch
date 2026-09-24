from django import forms

from .models import Job
from projects.models import Project


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = [
            "project",
            "title",
            "description",
            "required_skills",
            "job_type",
            "location",
            "number_of_workers",
            "application_deadline",
        ]

        widgets = {
            "project": forms.Select(attrs={
                "class": "form-input",
            }),

            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. Masonry Worker",
            }),

            "description": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Describe the job and responsibilities...",
                "rows": 5,
            }),

            "required_skills": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "e.g. Masonry, brick laying, concrete work...",
                "rows": 4,
            }),

            "job_type": forms.Select(attrs={
                "class": "form-input",
            }),

            "location": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. Mombasa, Kenya",
            }),

            "number_of_workers": forms.NumberInput(attrs={
                "class": "form-input",
                "min": "1",
            }),

            "application_deadline": forms.DateInput(attrs={
                "class": "form-input",
                "type": "date",
            }),
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)

        if company is not None:
            self.fields["project"].queryset = Project.objects.filter(
                company=company
            )

from django import forms
from .models import Job, JobApplication


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication
        fields = ["cover_message"]

        widgets = {
            "cover_message": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Tell the company why you are suitable for this job..."
                }
            )
        }

        labels = {
            "cover_message": "Cover Message",
        }

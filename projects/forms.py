from django import forms

from .models import Project, Attendance


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            "name",
            "location",
            "description",
            "status",
            "progress",
            "start_date",
            "expected_completion_date",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Project name"
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "placeholder": "Project location"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": (
                        "Describe the construction project..."
                    ),
                }
            ),

            "progress": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 100,
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "expected_completion_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance

        fields = [
            "status",
            "notes",
        ]

        widgets = {
            "status": forms.Select(),

            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Optional attendance note..."
                    ),
                }
            ),
        }
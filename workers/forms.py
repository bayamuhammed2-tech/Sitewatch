from django import forms

from .models import WorkerProfile


class WorkerProfileForm(forms.ModelForm):
    class Meta:
        model = WorkerProfile
        fields = [
            "phone_number",
            "location",
            "skills",
            "years_of_experience",
            "availability",
            "bio",
        ]

        widgets = {
            "phone_number": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. 0712345678",
            }),
            "location": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. Mombasa, Kenya",
            }),
            "skills": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "e.g. Masonry, plumbing, carpentry...",
                "rows": 4,
            }),
            "years_of_experience": forms.NumberInput(attrs={
                "class": "form-input",
                "min": "0",
                "placeholder": "Years of experience",
            }),
            "availability": forms.Select(attrs={
                "class": "form-input",
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Tell employers about yourself...",
                "rows": 5,
            }),
        }
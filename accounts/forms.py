from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        # Remove password1 and password2 from this list
        fields = (
            "username",
            "email",
            "role",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email address"
        self.fields["role"].label = "Account type"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm password"

        self.fields["role"].help_text = (
            "Choose Worker if you are looking for construction jobs, "
            "or Company if you want to hire workers and manage projects."
        )

        # Add CSS classes and placeholders
        self.fields["username"].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Enter your username",
        })

        self.fields["email"].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Enter your email address",
        })

        self.fields["role"].widget.attrs.update({
            "class": "form-input",
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Create a password",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Confirm your password",
        })
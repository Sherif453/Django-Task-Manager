from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    """A form bound to Task model; renders HTML inputs; handles validation.
    We customize the due_date widget to be 'datetime-local' for a nice browser picker."""
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "completed"]
        widgets = {
            # datetime-local expects a string like "2025-09-01T12:30"
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

class RegisterForm(UserCreationForm):
    """Built-in secure form to create a user with password hashing + validations."""
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

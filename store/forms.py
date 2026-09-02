from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomerProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

class CustomerProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
    )

    email = forms.EmailField(
        required=True,
    )

    class Meta:
        model = CustomerProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=commit)

        user = profile.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save(
                update_fields=[
                    "first_name",
                    "last_name",
                    "email",
                ]
            )

        return profile

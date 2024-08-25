# Django
from django import forms
from django.forms import ModelForm

# First Party
from dogs.models import SponsorSubmission
from pages.models import ContactSubmission, FosteringSubmission


class ContactForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data["consent"]:
            self.add_error(
                "consent",
                "You need to agree to us collecting your details if you want us to answer your enquiry",
            )

    class Meta:
        model = ContactSubmission
        fields = [
            "name",
            "email",
            "phone",
            "enquiry",
            "consent",
        ]


class SponsorForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data["consent"]:
            self.add_error(
                "consent",
                "You need to agree to us collecting your details if you want us to answer your enquiry",
            )

    class Meta:
        model = SponsorSubmission
        fields = [
            "name",
            "email",
            "phone",
            "dog",
            "sponsor_level",
            "comments",
            "consent",
        ]
        widgets = {"dog": forms.HiddenInput(), "sponsor_level": forms.RadioSelect()}


class FosteringForm(ModelForm):
    class Meta:
        model = FosteringSubmission
        fields = [
            "name",
            "email",
            "contact_number",
        ]

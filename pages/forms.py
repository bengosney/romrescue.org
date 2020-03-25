from django.forms import ModelForm
from django import forms

from .models import ContactSubmission, FosteringSubmission, IntrestSubmission, SponsorSubmission


class ContactForm(ModelForm):
    def clean(self):
        cleaned_data = super(ContactForm, self).clean()

        if not cleaned_data.get('consent'):
            self.add_error('consent', "You need to agree to us collecting your details if you want us to answer your enquiry")

    class Meta:
        model = ContactSubmission
        fields = '__all__'


class SponsorForm(ModelForm):
    def clean(self):
        cleaned_data = super(SponsorForm, self).clean()

        if not cleaned_data['consent']:
            raise forms.ValidationError("You need to agree to us collecting your details if you want us to answer your enquiry")

    class Meta:
        model = SponsorSubmission
        fields = '__all__'
        widgets = {'dog': forms.HiddenInput()}


class FosteringForm(ModelForm):
    class Meta:
        model = FosteringSubmission
        fields = '__all__'


class IntrestForm(ModelForm):
    class Meta:
        model = IntrestSubmission
        fields = '__all__'

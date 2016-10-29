from django.forms import ModelForm

from .models import ContactSubmission, FosteringSubmission


class ContactForm(ModelForm):

    class Meta:
        model = ContactSubmission
        fields = '__all__'


class FosteringForm(ModelForm):

    class Meta:
        model = FosteringSubmission
        fields = '__all__'

from django.forms import ModelForm

from .models import ContactSubmission


class ContactForm(ModelForm):
    success = 'Thank you for enquirying, we will be incontact soon.'

    class Meta:
        model = ContactSubmission
        fields = '__all__'

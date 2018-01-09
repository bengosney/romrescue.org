from django.forms import ModelForm
from django import forms

from .models import ContactSubmission, FosteringSubmission, IntrestSubmission


class ContactForm(ModelForm):

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        
        if cleaned_data['consent'] == False:
            raise forms.ValidationError("You need to agree to us collecting your details if you want us to answer your enquiry")
    
    class Meta:
        model = ContactSubmission
        fields = '__all__'


class FosteringForm(ModelForm):

    class Meta:
        model = FosteringSubmission
        fields = '__all__'


class IntrestForm(ModelForm):
    
    class Meta:
        model = IntrestSubmission
        fields = '__all__'

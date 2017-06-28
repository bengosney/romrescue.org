from django.forms import ModelForm

from .models import submission

class SubmissionForm(ModelForm):
    class Meta:
        model = submission
        exclude = []

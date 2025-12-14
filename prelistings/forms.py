"""
Forms for submitting installation requests.
"""
from django.forms import ModelForm, Select, Textarea
from .models import InstallationRequest

class InstallationRequestForm(ModelForm):
    """
    Form for initial request submission by Renters.
    """
    class Meta:
        model = InstallationRequest
        fields = ('environment_conditions', 'description')
        widgets = {
            'environment_conditions': Select(attrs = {'class': 'form-select'}),
            'description': Textarea(attrs = {'class': 'form-control'})
        }

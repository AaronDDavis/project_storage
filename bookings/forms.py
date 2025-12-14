"""
Forms for creating and managing bookings.
"""
from django.forms import ModelForm, DateInput
from .models import Booking

class BookingForm(ModelForm):
    """
    Form for capturing booking dates.

    Applies date-picker widgets to the input fields.
    """
    class Meta():
        model = Booking
        fields = ('start_date', 'end_date', )
        widgets = {
            'start_date': DateInput(attrs = {'class': 'form-control', 'id': 'book-start-date', 'type': 'date'}),
            'end_date': DateInput(attrs = {'class': 'form-control', 'id': 'book-end-date', 'type': 'date'}),
        }

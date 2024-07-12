from django import forms
from events.models import Event


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'email', 'autocomplete': 'off', 'placeholder': 'ex. hello@example.com'})
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'email', 'autocomplete': 'off', 'placeholder': 'ex. hello@example.com'})
    )


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        model = Event
        fields = [
            'title',
            'venue',
            'city',
            'start_date',
            'start_time',
            'end_time',
            'continuous',
            'end_date',
            'admission_price',
            'url',
            'extra_info',
        ]
        labels = {
            'title': 'Title *',
            'venue': 'Venue *',
            'city': 'City *',
            'start_date': 'Start Date *',
            'start_time': 'Start Time *',
            'end_time': 'End Time',
            'end_date': 'Final Date of Event (Setting a final date will create identical listings for each date from the start date to the final date of the event)',
            'continuous': 'Does this event last multiple days?',
            'extra_info': 'Any additional info (age range, sold out, byob, etc.)',
            'url': 'URL'
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'continuous': forms.CheckboxInput(),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

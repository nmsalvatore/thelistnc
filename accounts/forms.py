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
            # 'end_date',
            'admission_price',
            'url',
        ]
        labels = {
            'title': 'Title *',
            'venue': 'Venue *',
            'city': 'City *',
            'start_date': 'Start Date *',
            'start_time': 'Start Time *',
            'end_time': 'End Time',
            'end_date': 'End Date',
            'url': 'URL'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'ex. Aaron Ross'}),
            'venue': forms.TextInput(attrs={'placeholder': 'ex. Miner\'s Foundry'}),
            'city': forms.TextInput(attrs={'placeholder': 'ex. Nevada City'}),
            'admission_price': forms.TextInput(attrs={'placeholder': 'ex. $25'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'url': forms.TextInput(attrs={'placeholder': 'ex. https://www.minersfoundry.com/events/aaron-ross-show.html'}),
        }

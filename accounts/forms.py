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
            'end_date',
            'admission_price',
            'url',
        ]
        labels = {
            'title': 'Title *',
            'venue': 'Venue *',
            'city': 'City *',
            'start_date': 'Start Date & Time *',
            'end_date': 'End Date & Time',
            'url': 'URL'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'ex. Aaron Ross'}),
            'venue': forms.TextInput(attrs={'placeholder': 'ex. Miner\'s Foundry'}),
            'city': forms.TextInput(attrs={'placeholder': 'ex. Nevada City'}),
            'admission_price': forms.TextInput(attrs={'placeholder': 'ex. $25'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'url': forms.TextInput(attrs={'placeholder': 'ex. https://www.minersfoundry.com/events/aaron-ross-show.html'}),
        }

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
    class Meta:
        model = Event
        fields = [
            'title', 
            'venue', 
            'city', 
            'admission_price', 
            'start_date', 
            'end_date',
            'url',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'ex. Aaron Ross & Kendrick Lamar'}),
            'venue': forms.TextInput(attrs={'placeholder': 'ex. The Miner\'s Foundry'}),
            'city': forms.TextInput(attrs={'placeholder': 'ex. Nevada City'}),
            'admission_price': forms.NumberInput(attrs={'placeholder': 'ex. 25'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'url': forms.TextInput(attrs={'placeholder': 'ex. https://www.minersfoundry.com/events/aaron-ross-show.html'}),
        }


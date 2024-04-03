from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'email', 'autocomplete': 'off'})
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'email', 'autocomplete': 'off'})
    )

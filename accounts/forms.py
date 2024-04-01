from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True)


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)

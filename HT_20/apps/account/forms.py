from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "type": "text",
            "placeholder": 'Username',
            "class": "form-control",
            "autofocus": True,
        })
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            "type": "password",
            "placeholder": 'password',
            "class": "form-control",
            "autocomplete": "current-password",
        }),
    )

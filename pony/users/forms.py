from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    """Registration sign up form."""
    username = forms.CharField(max_length=30)
    password = forms.CharField(min_length=4, max_length=50, widget=forms.PasswordInput)
    password_confirm = forms.CharField(min_length=4, max_length=50, widget=forms.PasswordInput, label='Confirm')

    def clean_username(self):
        # Ensure username is lowercased and is not taken.
        username = self.cleaned_data['username']
        if username:
            username = username.lower()
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError('That username is already taken.')
        return username

    def clean(self):
        # Verify that the passwords matched.
        password1 = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password_confirm', None)
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Your passwords must match.')
        return self.cleaned_data

class LoginForm(forms.Form):
    """User login form."""
    username = forms.CharField(max_length=30)
    password = forms.CharField(min_length=4, max_length=50, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self._user = None

    def clean_username(self):
        # Ensure username is lowercased
        username = self.cleaned_data['username']
        if username:
            username = username.lower()
        return username

    def clean(self):
        # Validate the login credentials
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if username and password:
            self._user = auth.authenticate(username=username, password=password)
            if self._user is None:
                raise forms.ValidationError('Incorrect login.')
            elif not self._user.is_active:
                raise forms.ValidationError('That account is inactive.')
        return self.cleaned_data

    def get_user(self):
        return self._user

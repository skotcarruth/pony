from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    """Registration sign up form."""
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=30)
    password = forms.CharField(min_length=4, max_length=50, widget=forms.PasswordInput)
    password_confirm = forms.CharField(min_length=4, max_length=50, widget=forms.PasswordInput, label='Confirm')
    birthday = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))

    facebook_token = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean_email(self):
        # Ensure email is lowercased and is not taken.
        email = self.cleaned_data['email']
        if email:
            email = email.lower()
        try:
            User.objects.get(username=email)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError('That username is already taken.')
        return email

    def clean(self):
        # Verify that the passwords matched.
        password1 = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password_confirm', None)
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Your passwords must match.')
        return self.cleaned_data

class LoginForm(forms.Form):
    """User login form."""
    email = forms.EmailField(max_length=30)
    password = forms.CharField(min_length=4, max_length=50, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self._user = None

    def clean_email(self):
        # Ensure email is lowercased
        email = self.cleaned_data['email']
        if email:
            email = email.lower()
        return email

    def clean(self):
        # Validate the login credentials
        email = self.cleaned_data.get('email', None)
        password = self.cleaned_data.get('password', None)
        if email and password:
            self._user = auth.authenticate(username=email, password=password)
            if self._user is None:
                raise forms.ValidationError('Incorrect login.')
            elif not self._user.is_active:
                raise forms.ValidationError('That account is inactive.')
        return self.cleaned_data

    def get_user(self):
        return self._user

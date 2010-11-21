import calendar
import locale

from django import forms

from pony.teaser.models import TeaserSignup


LEAP_YEAR = 2012 # Ensures that we allow day 29 in February

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class TeaserSignupForm(forms.ModelForm):
    """Form for entering teaser signup info."""
    birthday_month = forms.TypedChoiceField(choices=[(None, 'month')] + TeaserSignup.MONTH_CHOICES,
        coerce=int, empty_value=None, error_messages={'invalid_choice': 'This field is required.'})
    birthday_day = forms.TypedChoiceField(choices=[(None, 'day')] + TeaserSignup.DAY_CHOICES,
        coerce=int, empty_value=None, error_messages={'invalid_choice': 'This field is required.'})

    class Meta:
        model = TeaserSignup
        fields = ('name', 'email', 'birthday_month', 'birthday_day',)

    def clean_email(self):
        # Ensure email doesn't exist yet
        email = self.cleaned_data['email']
        if email:
            email = email.lower()
        try:
            TeaserSignup.objects.get(email=email)
        except TeaserSignup.DoesNotExist:
            pass
        else:
            raise forms.ValidationError('We\'ve already got your email. Thanks!')
        return email

    def clean(self):
        # Verify that we have a valid date for birthday
        month = self.cleaned_data.get('birthday_month', None)
        day = self.cleaned_data.get('birthday_day', None)
        if month and day:
            if day > calendar.monthrange(LEAP_YEAR, month)[1]:
                raise forms.ValidationError('%s does not have %s days in it.' % (calendar.month_name[month], day))
        return self.cleaned_data

from django import forms

from pony.gifts.models import Gift


class GiftForm(forms.ModelForm):
    """Form for creating a new gift request."""
    class Meta:
        model = Gift
        fields = ('name', 'description', 'price', 'image',)

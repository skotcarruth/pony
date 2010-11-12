from django import forms

from pony.gifts.models import Gift


class GiftForm(forms.ModelForm):
    """Form for creating a new gift request."""
    name = forms.CharField(label='What I Want')
    price = forms.CharField(label='What It Costs')
    image = forms.ImageField(label='What It Looks Like', required=False)
    description = forms.CharField(label='Why I Want It', widget=forms.Textarea, required=False)

    class Meta:
        model = Gift
        fields = ('name', 'price', 'image', 'description',)

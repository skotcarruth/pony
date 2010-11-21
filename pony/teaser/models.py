import calendar
import locale

from django.db import models


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class TeaserSignup(models.Model):
    """A user who signs up on our teaser page."""
    MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
    DAY_CHOICES = [(i, str(i)) for i in range(1, 32)]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birthday_month = models.PositiveIntegerField(choices=MONTH_CHOICES)
    birthday_day = models.PositiveIntegerField(choices=DAY_CHOICES)

    created_ts = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_ts',)

    def __unicode__(self):
        return self.name

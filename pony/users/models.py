from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Extra profile information about a user."""
    user = models.OneToOneField(User)

    name = models.CharField(max_length=100)
    birthday = models.DateField()
    facebook_token = models.CharField(max_length=200, blank=True, null=True)
    twitter_username = models.CharField(max_length=200, blank=True, null=True)
    twitter_user_id = models.CharField(max_length=200, blank=True, null=True)
    twitter_token = models.CharField(max_length=200, blank=True, null=True)
    twitter_token_secret = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    def last_birthday(self, override_now=None):
        now = override_now or datetime.utcnow() # Override for testing
        last_birthday = self.birthday.replace(year=now.year)
        if now.date() <= last_birthday:
            last_birthday = last_birthday.replace(year=now.year - 1)
        return last_birthday

    def next_birthday(self, override_now=None):
        last_birthday = self.last_birthday(override_now=override_now)
        next_birthday = last_birthday.replace(year=last_birthday.year + 1)
        return next_birthday

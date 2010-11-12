from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Extra profile information about a user."""
    user = models.OneToOneField(User)

    name = models.CharField(max_length=100)
    birthday = models.DateField()
    facebook_token = models.CharField(max_length=200, blank=True, null=True)
    twitter_token = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.user.username

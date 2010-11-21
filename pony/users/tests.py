from datetime import date, datetime, timedelta
import uuid

from django.contrib.auth.models import User
from django.test import TestCase

from pony.gifts.models import Gift
from pony.users.models import UserProfile
from pony.users.views import user_can_add_gift


def create_user(**kwargs):
    email = 'test_%s@a.a' % str(uuid.uuid4()).replace('-', '')[::2]
    default = {
        'username': email,
        'password': 'test',
        'email': email,
    }
    default.update(kwargs)
    user = User.objects.create_user(default['username'], default['email'], default['password'])
    user.save()
    return user

def create_profile(user, **kwargs):
    default = {
        'user': user,
        'name': 'Test',
        'birthday': date(1985, 8, 18),
    }
    default.update(kwargs)
    profile = UserProfile(**default)
    profile.save()
    return profile

def create_gift(user, **kwargs):
    default = {
        'user': user,
        'status': 'active',
        'description': 'Test description',
        'price': 1,
        'gift_date': date(2010, 8, 18),
        'name': 'Test Gift',
    }
    default.update(kwargs)
    gift = Gift(**default)
    gift.save()
    return gift

class TestUserLogic(TestCase):
    def test_user_can_add_gift(self):
        u = create_user()
        create_profile(u, birthday=date(1985, 6, 1))
        create_gift(u, gift_date=date(2010, 6, 1))
        self.assertTrue(user_can_add_gift(u, override_now=datetime(2010, 7, 1)))
        self.assertFalse(user_can_add_gift(u, override_now=datetime(2010, 5, 1)))

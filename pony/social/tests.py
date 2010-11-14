import json

from django.contrib.auth.models import User
from django.test import TestCase


class TestTwitterOAuth(TestCase):
    fixtures = ['twitter_oauth.json']

    def test_authorize_url_view(self):
        response = self.client.get('/social/oauth/twitter/authorize-url/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data.keys(), ['authorize_url'])

    def test_callback_view(self):
        # Test facebook callback
        response = self.client.get('/social/callback/facebook/')
        self.assertEqual(response.status_code, 200)

        # Test twitter callback errors
        response = self.client.get('/social/callback/twitter/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], None)
        response = self.client.get('/social/callback/twitter/?oauth_token=crap&oauth_verifier=morecrap')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], None)

    def test_access_resource(self):
        # Log in a user with twitter creds, then request a resource
        self.client.login(username='test', password='test')
        response = self.client.get('/social/oauth/twitter/GET/users/show/?user_id=72725663&screen_name=jeffschenck')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['name'], 'Jeff Schenck')

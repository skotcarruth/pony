import json
import oauth2 as oauth
import urllib
import urlparse

from django.conf import settings


class HandlerException(Exception):
    pass

class MissingRequestToken(HandlerException):
    pass

class MissingAccessToken(HandlerException):
    pass

class ServiceError(HandlerException):
    pass

class TwitterOAuth(object):
    """Common interface for OAuth and talking to social services."""
    REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
    AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'

    # Replace with (category, resource)
    RESOURCE_URL = 'http://api.twitter.com/1/%s/%s.json'

    def __init__(self, oauth_token=None, oauth_token_secret=None):
        self.request_token = None
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    def get_request_token(self, callback_url=None):
        consumer = oauth.Consumer(settings.TWITTER_KEY, settings.TWITTER_SECRET)
        client = oauth.Client(consumer)
        body = None
        if callback_url:
            body = urllib.urlencode({'oauth_callback': callback_url})
        resp, content = client.request(self.REQUEST_TOKEN_URL, 'POST', body=body)
        self.request_token = dict(urlparse.parse_qsl(content))

    def get_authorize_url(self):
        if not self.request_token:
            raise MissingRequestToken('You must request a request token first.')
        authorize_url = '%s?oauth_token=%s' % (
            self.AUTHORIZE_URL,
            self.request_token['oauth_token'],
        )
        return authorize_url

    def get_access_token(self, oauth_token, oauth_verifier):
        # Query twitter for the access token
        consumer = oauth.Consumer(settings.TWITTER_KEY, settings.TWITTER_SECRET)
        token = oauth.Token(oauth_token, settings.TWITTER_SECRET)
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer, token)
        resp, content = client.request(self.ACCESS_TOKEN_URL, 'POST')

        # Test for success or error response
        if resp['status'] != '200' or '<error>' in content:
            raise ServiceError(content)
        self.access_token = dict(urlparse.parse_qsl(content))
        return self.access_token

    def access_resource(self, category, resource, params={}, method='GET'):
        # Construct the url to query
        url = self.RESOURCE_URL % (category, resource)
        resource = '%s?%s' % (url, urllib.urlencode(params))
        consumer = oauth.Consumer(settings.TWITTER_KEY, settings.TWITTER_SECRET)
        token = oauth.Token(key=self.oauth_token, secret=self.oauth_token_secret)
        client = oauth.Client(consumer, token)

        # Query the API and parse the json
        resp, content = client.request(resource, method)
        return json.loads(content)

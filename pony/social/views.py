from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response

from pony.decorators import json_response
from pony.social.oauth import TwitterOAuth, ServiceError


def callback(request, service=None):
    """Callback for Facebook and Twitter OAuth."""
    if service == 'facebook':
        return render_to_response('social/facebook_callback.html')

    elif service == 'twitter':
        oauth_token = request.GET.get('oauth_token', None)
        oauth_verifier = request.GET.get('oauth_verifier', None)
        if not oauth_token or not oauth_verifier:
            # Fucked
            messages.error(request, 'Invalid OAuth callback. Please try again.')
            return render_to_response('social/twitter_callback.html', {'user': None})

        oauth = TwitterOAuth()
        try:
            access_token = oauth.get_access_token(oauth_token, oauth_verifier)
        except ServiceError:
            # Fucked
            messages.error(request, 'Invalid OAuth callback. Please try again.')
            return render_to_response('social/twitter_callback.html', {'user': None})

        # Score! Store the token on the session
        request.session['twitter_access_token'] = access_token
        return render_to_response('social/twitter_callback.html', {
            'user': {'username': access_token['screen_name'], 'user_id': access_token['user_id']},
        })

    raise Http404

@json_response
def authorize_url(request, service=None):
    """AJAX view to get an authorize url from twitter and return it."""
    callback_url = request.GET.get('callback_url',
        reverse('pony.social.views.callback', kwargs={'service': 'twitter'}))
    oauth = TwitterOAuth()
    oauth.get_request_token(callback_url=callback_url)
    authorize_url = oauth.get_authorize_url()
    return {'authorize_url': authorize_url}

@json_response
def access_resource(request, service=None, method=None, category=None, resource=None):
    """AJAX view to request a resource from twitter and return it."""
    if service == 'twitter':
        # Retrieve the token and secret from the session or from the user
        oauth_token = None
        oauth_token_secret = None
        session_access_token = request.session.get('twitter_access_token', None)
        if session_access_token:
            oauth_token = session_access_token['oauth_token']
            oauth_token_secret = session_access_token['oauth_token_secret']
        else:
            profile = request.user.get_profile()
            if profile:
                oauth_token = profile.twitter_token
                oauth_token_secret = profile.twitter_token_secret

        # If no token/secret, then oopsies
        if not oauth_token or not oauth_token_secret:
            raise Http404

        # Query for the resource
        oauth = TwitterOAuth(oauth_token, oauth_token_secret)
        return oauth.access_resource(category, resource, request.GET, method)

    raise Http404

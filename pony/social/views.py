from django.http import Http404
from django.shortcuts import render_to_response


def callback(request, service=None):
    """Callback for Facebook and Twitter OAuth."""
    if service == 'facebook':
        return render_to_response('social/facebook_callback.html')
    raise Http404

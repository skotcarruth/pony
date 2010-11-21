import random

from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from pony.teaser import forms
from pony.teaser.models import TeaserSignup


BDAY_PONY_ADJECTIVES = ['near', 'near', 'near', 'near', 'near', 'near', 'near',
    'near', 'close', 'close', 'close', 'close', 'close', 'close', 'clear',
    'happening', 'happening', 'happening', 'happening', 'partying', 'partying',
    'partying', 'partying', 'born', 'born', 'neigh', 'watching you',
    'imaginary... or is it', 'purebred', 'delivered',]

def teaser_index(request):
    """Home page with teaser text and signup form."""
    # Thank you message for users who signed up
    if request.session.pop('thanks', False):
        return render_to_response('teaser/teaser_thanks.html', {}, RequestContext(request))

    # Handle the signup form
    if request.method == 'POST':
        form = forms.TeaserSignupForm(request.POST)
        if form.is_valid():
            signup = form.save()
            request.session['thanks'] = True
            return redirect(teaser_index)
    else:
        form = forms.TeaserSignupForm()

    return render_to_response('teaser/teaser_index.html', {
        'form': form,
        'adjective': random.choice(BDAY_PONY_ADJECTIVES),
    }, RequestContext(request))

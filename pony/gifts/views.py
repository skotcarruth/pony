from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from pony.gifts import forms
from pony.gifts.models import Gift


def add(request):
    """Create a new gift request."""
    if request.method == 'POST':
        form = forms.GiftForm(request.POST)
        if form.is_valid():
            gift = form.save()
            request.session['gift'] = gift
            if request.user.is_authenticated():
                # Logged-in users should go directly to their gift page
                if request.user.is_active:
                    return redirect('pony.gifts.views.detail', gift_id=gift.id)
                else:
                    messages.error(request, 'Your account is not active.')
            else:
                # Non-logged-in users should either log in or register
                return redirect('pony.users.views.register')
    else:
        form = forms.GiftForm()

    return render_to_response('gifts/add.html', {
        'form': form,
    }, RequestContext(request))

def detail(request, gift_id=None):
    """View an existing gift request."""
    gift = get_object_or_404(Gift, pk=gift_id, status__in=Gift.VISIBLE_STATUSES)
    return render_to_response('gifts/detail.html', {
        'gift': gift,
    }, RequestContext(request))

def give(request, gift_id=None):
    """Give money toward a gift."""
    gift = get_object_or_404(Gift, pk=gift_id, status__in=Gift.VISIBLE_STATUSES)
    if request.user == gift.user:
        messages.error(request, 'You cannot give to your own gift.')
        return redirect(gift)

    return render_to_response('gifts/give.html', {
        'gift': gift,
    }, RequestContext(request))

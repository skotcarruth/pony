from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from pony.gifts import forms
from pony.gifts.models import Gift


def add(request):
    """Create a new gift request."""
    if request.method == 'POST':
        form = forms.GiftForm(request.POST, request.FILES)
        if form.is_valid():
            gift = form.save(commit=False)
            if request.user.is_authenticated():
                # Logged-in users should go directly to their gift page
                if request.user.is_active:
                    gift.user = request.user
                    gift.gift_date = request.user.get_profile().next_birthday()
                    gift.save()
                    return redirect(gift.get_absolute_url())
                else:
                    messages.error(request, 'Your account is not active.')
            else:
                # Non-logged-in users should either log in or register
                gift.save()
                request.session['gift'] = gift
                return redirect('pony.users.views.register')
    else:
        form = forms.GiftForm()

    return render_to_response('gifts/add.html', {
        'form': form,
    }, RequestContext(request))

def detail(request, gift_id=None):
    """View an existing gift request."""
    gift = get_object_or_404(Gift, pk=gift_id)
    if not gift.visible_to_user(request.user):
        raise Http404

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

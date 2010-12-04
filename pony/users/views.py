from datetime import datetime

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from pony.gifts.models import Gift
from pony.users import forms
from pony.users.models import UserProfile


def user_can_add_gift(user, override_now=None):
    """Returns true if the user is allowed to add a new gift."""
    try:
        profile = user.get_profile()
    except UserProfile.DoesNotExist:
        return False

    # Get all the gifts since the user's most recent birthday
    last_birthday = profile.last_birthday(override_now=override_now)
    return not Gift.objects.filter(user=user, gift_date__gt=last_birthday).exists()

def login(request):
    """User login page."""
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            auth.login(request, login_form.get_user())
            return redirect('pony.users.views.dashboard')
    else:
        login_form = forms.LoginForm()

    return render_to_response('users/login.html', {
        'login_form': login_form,
    }, RequestContext(request))

@login_required
def logout(request):
    """User logout and redirect."""
    auth.logout(request)
    return redirect('pony.views.index')

@login_required
def dashboard(request):
    """Allows a user to change settings and see things."""
    gifts = Gift.objects.filter(user=request.user)
    return render_to_response('users/dashboard.html', {
        'gifts': gifts,
        'can_add_gift': user_can_add_gift(request.user)
    }, RequestContext(request))

def register(request):
    """Sign up page."""
    # If you're already logged in, you shouldn't be here
    if request.user.is_authenticated():
        messages.error(request, 'You are already logged in.')
        return redirect('pony.users.views.dashboard')

    # Handle the registration form
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            # Create the user and log them in
            User.objects.create_user(
                register_form.cleaned_data['email'],
                register_form.cleaned_data['email'],
                register_form.cleaned_data['password'],
            )
            user = auth.authenticate(
                username=register_form.cleaned_data['email'],
                password=register_form.cleaned_data['password'],
            )
            auth.login(request, user)

            # Create the user profile
            user_profile = UserProfile(
                user=user,
                name=register_form.cleaned_data['name'],
                birthday=register_form.cleaned_data['birthday'],
                facebook_token=register_form.cleaned_data['facebook_token'],
            )
            # Grab the twitter auth info from the session, if it's there
            session_access_token = request.session.get('twitter_access_token', None)
            if session_access_token:
                user_profile.twitter_username = session_access_token['screen_name']
                user_profile.twitter_user_id = session_access_token['user_id']
                user_profile.twitter_token = session_access_token['oauth_token']
                user_profile.twitter_token_secret = session_access_token['oauth_token_secret']
            # Save the profile
            user_profile.save()

            # If the user session has a gift on it, redirect there
            gift = request.session.get('gift', None)
            if gift:
                # Determine the gift date based on the current date
                next_birthday = user_profile.birthday.replace(year=datetime.utcnow().year)
                if datetime.utcnow().date() > next_birthday:
                    next_birthday.replace(year=datetime.utcnow().year + 1)

                # Fill in the gift details for this user
                gift.user = user
                gift.gift_date = next_birthday
                gift.status = gift.ACTIVE
                gift.save()
                del request.session['gift']
                return redirect(gift)

            return redirect('pony.users.views.dashboard')
    else:
        register_form = forms.RegisterForm()

    return render_to_response('users/register.html', {
        'gift': request.session.get('gift', None),
        'register_form': register_form,
    }, RequestContext(request))

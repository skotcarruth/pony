from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from pony.users import forms


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
    return render_to_response('users/dashboard.html', {
    }, RequestContext(request))

# def register(request):
#     """Sign up page."""
#     if request.user.is_authenticated():
#         messages.error(request, 'You are already logged in. Please log out before registering.')
#         return redirect('hawbnawb.views.home')
# 
#     if request.method == 'POST':
#         register_form = forms.RegisterForm(request.POST)
#         if register_form.is_valid():
#             User.objects.create_user(
#                 register_form.cleaned_data['username'],
#                 register_form.cleaned_data['email'],
#                 register_form.cleaned_data['password'],
#             )
#             user = auth.authenticate(
#                 username=register_form.cleaned_data['username'],
#                 password=register_form.cleaned_data['password'],
#             )
#             auth.login(request, user)
#             return redirect('hawbnawb.accounts.views.add')
#     else:
#         register_form = forms.RegisterForm()
# 
#     return render_to_response('users/register.html', {
#         'register_form': register_form,
#     }, RequestContext(request))

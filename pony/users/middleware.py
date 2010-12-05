from pony.views import index


class NewUserMiddleware(object):
    """
    Determines wither the request is from a new user. MUST come AFTER the 
    session middleware in the stack to work properly. 
    """
    def process_request(self, request):
        # If new_user isn't on the session, assume they're a new user
        if hasattr(request, 'session') \
        and 'new_user' not in request.session \
        and not request.user.is_authenticated():
            request.session['new_user'] = True

    def process_view(self, request, view_func, view_args, view_kwargs):
        # If the new user enters on the homepage, don't specially mark them
        if hasattr(request, 'session') and view_func is index:
            request.session['new_user'] = False

    def process_response(self, request, response):
        # After processing any request, the user is no longer new
        if hasattr(request, 'session'):
            request.session['new_user'] = False
        return response

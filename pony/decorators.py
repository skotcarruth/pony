import functools
import json

from django.http import HttpResponse


def json_response(view):
    """
    The view function should return a normal Python object (JSON-serializable,
    please). The wrapper will then convert this to JSON and return an
    appropriate HttpResponse object.
    """
    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        data = view(request, *args, **kwargs)
        return HttpResponse(json.dumps(data), mimetype='application/javascript')
    return wrapper

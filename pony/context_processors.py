from django.conf import settings


def settings_object(request):
    """Adds the django settings to the context."""
    return {'settings': settings}

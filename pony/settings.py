"""
Super-complicated-but-simple settings loader!

This settings.py file should live in your project directory alongside
manage.py so Django uses it. You should also have an env directory, with an
__init__.py, a settings_base.py, a settings_local.py, and any number of
settings_[env].py files. (It is recommended that you ignore your
settings_local.py file in your version control setup.)

The settings_base.py file should contain all your base settings, which can
then be overridden by your environment-specific settings and your local
settings. Create a settings_[env].py file for each of your environments
(e.g., settings_dev.py, settings_staging.py, settings_prod.py). In each, you
may override base settings with new settings you want in that environment.

In settings_local.py, you are only required to do one thing: define the ENV
setting. For example:

DEV = 'env'

You may also add any final overrides to settings that should be specific to
that particular box.
"""

# Import all the base settings
try:
    from env.settings_base import *
except ImportError:
    # Django clobbers import errors with a "helpful" message
    raise ValueError('Cannot find env/settings_base.py in your project.')

# Import the environment-specific settings
try:
    from env.settings_local import ENV
except ImportError:
    raise ValueError('Cannot find env/settings_local.py in your project or '
        'settings_local does not have ENV defined.')

path = 'env.settings_%s' % ENV
try:
    env_settings = __import__(path, globals(), locals(), [], -1)
except ImportError:
    raise ValueError('Cannot find env/settings_[env].py file with the ENV '
        'defined in env/settings_local.py.')

for key, value in vars(getattr(env_settings, 'settings_%s' % ENV)).iteritems():
    if not key.startswith('_'):
        globals()[key] = value

# Override with any settings in local_settings
from env.settings_local import *

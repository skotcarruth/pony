# Settings overrides for the prod environment
DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pony',
        'USER': 'www',
        'PASSWORD': 'pony',
        'HOST': '',
        'PORT': '',
    }
}

# FACEBOOK_APP_ID = '108483569216902'
# FACEBOOK_APP_SECRET = '5d33dc46eddfecd7da9e6dc29ae7b16b'
# 
# TWITTER_KEY = 'oMYdtZhZMJEsitBieXDmMQ'
# TWITTER_SECRET = 'Y11rk0m8ClbLcxRQd3NsbrXVB5ufaoLHwNt9Z3q2GA'

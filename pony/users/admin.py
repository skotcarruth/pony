from django.contrib import admin

from pony.users.models import UserProfile


admin.site.register(UserProfile)

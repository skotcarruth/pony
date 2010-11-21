from django.contrib import admin

from pony.teaser.models import TeaserSignup


class TeaserSignupAdmin(admin.ModelAdmin):
    fieldsets = (
        ('User Info', {
            'fields': ('name', 'email', 'birthday_month', 'birthday_day'),
        }),
        ('Metadata', {
            'fields': ('created_ts',),
        }),
    )
    readonly_fields = ('name', 'email', 'birthday_month', 'birthday_day', 'created_ts',)
    date_hierarchy = 'created_ts'
    list_display = ('name', 'email', 'created_ts',)
    list_filter = ('created_ts',)
    search_fields = ('name', 'email',)

admin.site.register(TeaserSignup, TeaserSignupAdmin)

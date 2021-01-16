from django.contrib import admin

from pages import models


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PageAnalytics)
class PageAnalyticsAdmin(admin.ModelAdmin):
    fields = ('page', 'ip_addr', 'date', 'lat', 'lng', 'country', 'city')
    readonly_fields = ('date',)

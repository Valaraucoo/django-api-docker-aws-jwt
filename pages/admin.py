from django.contrib import admin

from pages import models


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    pass


class AnalyticsBaseAdmin(admin.ModelAdmin):
    fields = ('page', 'ip_addr', 'date', 'lat', 'lng', 'country', 'city')
    readonly_fields = ('date',)


@admin.register(models.PageAnalytics)
class PageAnalyticsAdmin(AnalyticsBaseAdmin):
    pass


@admin.register(models.MainPageAnalytics)
class MainPageAnalyticsAdmin(AnalyticsBaseAdmin):
    pass


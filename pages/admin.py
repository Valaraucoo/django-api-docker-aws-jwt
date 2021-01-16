from django.contrib import admin

from pages import models


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    pass

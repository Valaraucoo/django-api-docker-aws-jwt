import datetime
import uuid

from django.db import models
from django.template.defaultfilters import slugify


PAGE_TYPES_CHOICES = (
    ('INDUSTRY', 'industry'),
    ('SERVICES', 'services'),
    ('ENGINEERING', 'engineering'),
)


class Page(models.Model):
    user = models.ForeignKey('users.User', related_name='pages', on_delete=models.CASCADE)
    is_created = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True, unique=True)

    name = models.CharField(max_length=30, default='')
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES_CHOICES, default='')
    contact_email = models.CharField(max_length=100, default='')

    header_title = models.CharField(max_length=30, default='')
    header_description = models.CharField(max_length=255, default='')

    services_enable = models.BooleanField(default=False)
    services_title = models.CharField(max_length=30, default='')
    services_description = models.CharField(max_length=255, default='')

    services_1_type = models.CharField(max_length=30, default='')
    services_1_title = models.CharField(max_length=30, default='')
    services_1_description = models.CharField(max_length=255, default='')

    services_2_type = models.CharField(max_length=30, default='')
    services_2_title = models.CharField(max_length=30, default='')
    services_2_description = models.CharField(max_length=255, default='')

    services_3_type = models.CharField(max_length=30, default='')
    services_3_title = models.CharField(max_length=30, default='')
    services_3_description = models.CharField(max_length=255, default='')

    about_enable = models.BooleanField(default=False)
    about_title = models.CharField(max_length=30, default='')
    about_subtitle = models.CharField(max_length=50, default='')
    about_description = models.TextField(null=True, blank=True)

    main_color = models.CharField(max_length=30, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    __name = None

    class Meta:
        ordering = ('name', 'page_type', 'updated_at',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__name = self.name

    def __str__(self) -> str:
        return f'Page: {self.name} ({self.page_type})'

    def save(self, *args, **kwargs):
        if self.__name != self.name:
            uid = str(uuid.uuid4())[:20]
            self.slug = slugify(f"{self.name}-{uid}")
        super().save(*args, **kwargs)

    @property
    def view_count(self) -> int:
        return self.analytics.count()

    @property
    def week_views_count(self) -> int:
        return self.analytics.filter(date__gt=datetime.datetime.now()-datetime.timedelta(days=7)).count()

    @property
    def month_views_count(self) -> int:
        return self.analytics.filter(date__gt=datetime.datetime.now()-datetime.timedelta(days=30)).count()


class Analytics(models.Model):
    ip_addr = models.CharField(max_length=30)

    lat = models.CharField(max_length=30)
    lng = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=255)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PageAnalytics(Analytics):
    page = models.ForeignKey('Page', related_name='analytics', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Page analytics: {self.page} {self.date}"


class MainPageAnalytics(Analytics):
    def __str__(self) -> str:
        return f"Main analytics: {self.date}"

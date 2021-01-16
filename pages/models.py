import uuid

from django.db import models
from django.template.defaultfilters import slugify


PAGE_TYPES_CHOICES = (
    ('INDUSTRY', 'industry'),
    ('SERVICES', 'services'),
    ('ENGINEERING', 'engineering'),
)


class Page(models.Model):
    user = models.OneToOneField('users.User', related_name='page', on_delete=models.CASCADE)
    is_created = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True, unique=True)

    name = models.CharField(max_length=30, default='')
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES_CHOICES, default='')

    header_title = models.CharField(max_length=30, default='')
    header_description = models.CharField(max_length=255, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', 'page_type', 'updated_at',)

    def __str__(self) -> str:
        return f'Page: {self.name} ({self.page_type})'

    def save(self, *args, **kwargs):
        if not self.slug:
            uid = str(uuid.uuid4())[:20]
            self.slug = slugify(f"{self.name}-{uid}")
        super().save(*args, **kwargs)

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from users import managers


GENDER_CHOICES = (
    ('male', _('Male')),
    ('female', _('Female')),
    ('none', 'none'),
)


class User(auth_models.AbstractUser):
    username = None

    first_name = models.CharField(max_length=30, blank=True, verbose_name=_('First name'))
    last_name = models.CharField(max_length=150, blank=True, verbose_name=_('Last name'))

    email = models.EmailField(unique=True, verbose_name=_('Email address'))
    phone = models.CharField(max_length=9, blank=True, verbose_name=_('Phone number'))
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(verbose_name=_('Date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',)

    objects = managers.CustomUserManager()

    @property
    def full_username(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

    def __str__(self):
        return self.full_username

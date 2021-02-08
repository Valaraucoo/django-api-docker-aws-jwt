import datetime
import os
import uuid

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from users.emails.emails import ResetPasswordEmail
from users import managers
from subscriptions.models import UserSubscription

GENDER_CHOICES = (
    ('male', _('Male')),
    ('female', _('Female')),
    ('none', 'none'),
)


def get_file_path(instance, filename: str) -> str:
    today = datetime.date.today().strftime("%Y-%m-%d")
    return os.path.join(settings.UPLOAD_FILES_DIR, today, str(uuid.uuid4()) + filename)


class User(auth_models.AbstractUser):
    username = None

    first_name = models.CharField(
        max_length=30, blank=True, verbose_name=_('First name'))
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name=_('Last name'))
    image = models.ImageField(upload_to=get_file_path,
                              default=settings.DEFAULT_PROFILE_IMAGE)

    email = models.EmailField(unique=True, verbose_name=_('Email address'))
    phone = models.CharField(max_length=9, blank=True,
                             verbose_name=_('Phone number'))
    address = models.CharField(max_length=255, blank=True)

    subscription = models.OneToOneField(
        UserSubscription, on_delete=models.CASCADE, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'), auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',)

    objects = managers.CustomUserManager()

    def __str__(self) -> str:
        return self.full_username

    @property
    def full_username(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

    def get_image_url(self) -> str:
        return self.image.url


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    ResetPasswordEmail().create_reset_password_email(user=reset_password_token.user,
                                                     token=reset_password_token.key).send()

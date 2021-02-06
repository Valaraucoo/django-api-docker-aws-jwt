import datetime

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from users.emails.emails import ResetPasswordEmail
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
    address = models.CharField(max_length=255, blank=True)
    subscription_to = models.DateTimeField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(verbose_name=_('Date joined'), auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',)

    objects = managers.CustomUserManager()

    def __str__(self) -> str:
        return self.full_username

    @property
    def full_username(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def is_subscriber(self) -> bool:
        if not self.subscription_to:
            return False
        return self.subscription_to.replace(tzinfo=None) - datetime.datetime.now() > datetime.timedelta(days=0)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    ResetPasswordEmail().create_reset_password_email(user=reset_password_token.user,
                                                     token=reset_password_token.key).send()

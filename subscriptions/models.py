from django.db import models
from datetime import datetime


class UserSubscription(models.Model):
    client_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255, blank=True, null=True)
    subscribed_until = models.DateTimeField(null=True, blank=True)

    @property
    def is_premium(self) -> bool:
        return self.subscribed_until and self.subscribed_until > datetime.now()

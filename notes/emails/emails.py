import datetime

from typing import Any, Dict, List

from django.core import mail

from emails import base_emails
from users import models as users_models
from notes import models as notes_models
from subscriptions import models as subscription_models


class PaymentMailFactory(base_emails.EmailFactoryInterface):
    user: users_models.User
    subscription: subscription_models.UserSubscription
    email_to: List[str]

    subject: str = "Payment Invoice"
    email_template_name: str = "emails/notes/payment-invoice.html"

    def create_invoice_mail(self, user: users_models.User,
                            subscription: subscription_models.UserSubscription) -> mail.EmailMessage:
        self.user = user
        self.subscription = subscription
        self.email_to = [self.user.email] + self.email_to

        return self.create_email()

    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        return {
            'user': self.user,
            'subscription': self.subscription,
        }


class PaymentNotificationMailFactory(base_emails.EmailFactoryInterface):
    user: users_models.User
    email_to: List[str]

    subject: str = "Payment Notification"
    email_template_name: str = "emails/notes/payment-notification.html"

    def create_notification_email(self, user) -> mail.EmailMessage:
        self.user = user
        self.email_to = [self.user.email] + self.email_to

        return self.create_email()

    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        try:
            days = (self.user.subscription.subscribed_until.replace(tzinfo=None) - datetime.datetime.now()).days
        except AttributeError:
            days = 0
        return {
            'user': self.user,
            'days': days
        }

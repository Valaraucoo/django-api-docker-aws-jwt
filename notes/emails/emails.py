import datetime

from typing import Any, Dict, List

from django.core import mail

from emails import base_emails
from users import models as users_models
from notes import models as notes_models


class PaymentMailFactory(base_emails.EmailFactoryInterface):
    user: users_models.User
    invoice: notes_models.PaymentInvoice
    email_to: List[str]

    subject: str = "Payment Invoice"
    email_template_name: str = "emails/notes/payment-invoice.html"

    def create_invoice_mail(self, user: users_models.User, invoice: notes_models.PaymentInvoice) -> mail.EmailMessage:
        self.user = user
        self.invoice = invoice
        self.email_to = [self.user.email] + self.email_to

        return self.create_email()

    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        return {
            'user': self.user,
            'invoice': self.invoice,
            'datetime': datetime.datetime.now() + datetime.timedelta(days=30)
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
            days = (self.user.subscription_to.replace(tzinfo=None) - datetime.datetime.now()).days
        except AttributeError:
            days = 0
        return {
            'user': self.user,
            'days': days
        }

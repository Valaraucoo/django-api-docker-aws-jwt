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
        self.email_to = [self.user.email]

        return self.create_email()

    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        return {
            'user': self.user,
            'invoice': self.invoice
        }

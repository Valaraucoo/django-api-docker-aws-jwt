import datetime

from typing import Any, Dict
from django.core import mail

from notes.emails.emails import PaymentMailFactory
from .base_documents import DocumentTemplateInterface


class PaymentInvoiceDocument(DocumentTemplateInterface):
    """
    PaymentInvoiceDocument implements DocumentTemplateInterface - is used to
    generate invoice document and allows you to send the generated e-mail
    via PaymentMailFactory.

    Usage:
    >>> PaymentInvoiceDocument(user, subscription).send()
    """
    template_name = "documents/notes/invoice.html"

    @property
    def filename(self) -> str:
        date = str(datetime.date.today()).replace('-', '_')
        return f"noteneo_invoice_{self.subscription.client_id}_{date}.pdf"

    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        return {
            'user': self.user,
            'subscription': self.subscription,
            'date': datetime.date.today()
        }

    def send(self, *args, **kwargs) -> None:
        message: mail.EmailMessage = PaymentMailFactory().\
            create_invoice_mail(user=self.user, subscription=self.subscription)
        pdf, bytes_pdf = self.get_document(*args, **kwargs)
        if pdf:
            message.attach(self.filename, bytes_pdf.getvalue())
        message.send()

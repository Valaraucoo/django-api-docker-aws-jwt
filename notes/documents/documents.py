from typing import Any, Dict

from django.core import mail

from notes.emails.emails import PaymentMailFactory
from notes.documents.base_documents import DocumentTemplateInterface


class PaymentInvoiceDocument(DocumentTemplateInterface):
    """
    Usage:
    >>> PaymentInvoiceDocument(user, invoice).send()
    """
    template_name = "documents/notes/invoice.html"
    filename = "NoteneoPaymentInvoice.pdf"

    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        return {
            'user': self.user,
            'invoice': self.invoice,
        }

    def send(self, *args, **kwargs) -> None:
        message: mail.EmailMessage = PaymentMailFactory().create_invoice_mail(user=self.user, invoice=self.invoice)
        pdf, bytes_pdf = self.get_document(*args, **kwargs)
        if pdf:
            message.attach(self.filename, bytes_pdf.getvalue())
        message.send()

from typing import List, Dict, Any

from django.conf import settings
from django.core import mail
from django.template import loader


class BaseEmail(object):
    subject: str
    email_template_name: str
    email_from: str = None
    cc: List[str] = None
    bcc: List[str] = None
    reply_to: List[str] = None

    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        raise NotImplementedError()

    def create_email(self, email_to: List[str], *args, **kwargs) -> mail.EmailMessage:
        context = self.get_context_data()
        body = loader.render_to_string(self.email_template_name, context)
        email_from = self.email_from or settings.SENDER_EMAIL
        message = mail.EmailMessage(self.subject, body, email_from, email_to,
                                    cc=self.cc, bcc=self.bcc, reply_to=self.reply_to)
        message.content_subtype = 'html'
        return message

    def send(self, email_to: List[str]) -> None:
        self.create_email(email_to=email_to).send()

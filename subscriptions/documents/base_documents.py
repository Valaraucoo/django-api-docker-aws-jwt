import abc
from typing import Dict, Any, Tuple
from io import BytesIO

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

from subscriptions.models import UserSubscription
from users.models import User


class DocumentTemplateInterface(abc.ABC):
    """
    DocumentTemplateInterface is used to generate invoice document and allows
    you to send the generated e-mail via Django Mail API.
    """
    template_name: str
    filename: str

    def __init__(self, user: User, subscription: UserSubscription):
        self.user = user
        self.subscription = subscription

    @abc.abstractmethod
    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        pass

    @abc.abstractmethod
    def send(self, *args, **kwargs) -> None:
        pass

    def get_document(self, *args, **kwargs) -> Tuple[pisa.pisaDocument, BytesIO]:
        context = self.get_context_data(*args, **kwargs)
        return self.render_pdf(context)

    def get_http_response(self, *args, **kwargs) -> HttpResponse:
        pdf, bytes_pdf = self.get_document(*args, **kwargs)
        if pdf:
            response = HttpResponse(bytes_pdf.getvalue(), content_type='application/pdf')
            content = f"inline; filename={self.filename}"
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found", status=404)

    def render_pdf(self, context: Dict[Any, Any]) -> Tuple[pisa.pisaDocument, BytesIO]:
        template = get_template(self.template_name)
        html = template.render(context)
        result = BytesIO()
        return pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result), result

import abc
from typing import Dict, Any, Tuple
from io import BytesIO

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa


class DocumentTemplateInterface(abc.ABC):
    template_name: str
    filename: str

    def __init__(self, template_name: str, filename: str):
        self.template_name = template_name
        self.filename = filename

    @abc.abstractmethod
    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        pass

    def save(self, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(*args, **kwargs)
        pdf, bytes_pdf = self._generate_document(context)
        if pdf:
            response = HttpResponse(bytes_pdf.getvalue(), content_type='application/pdf')
            content = f"inline; filename={self.filename}"
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found", status=404)

    def _generate_document(self, context: Dict[Any, Any]) -> Tuple[pisa.pisaDocument, BytesIO]:
        template = get_template(self.template_name)
        html = template.render(context)
        result = BytesIO()
        return pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result), result

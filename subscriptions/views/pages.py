from django.views.generic.base import TemplateView


class SuccessPaymentView(TemplateView):
    template_name = "subscriptions/success.html"


class FailedPaymentView(TemplateView):
    template_name = "subscriptions/failed.html"

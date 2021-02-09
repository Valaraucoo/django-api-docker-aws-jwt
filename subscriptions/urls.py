from django.urls import path, include
from .views.stripe import StripeWebhook
from .views.pages import SuccessPaymentView, FailedPaymentView

app_name = 'subscriptions'

urlpatterns = [
    path('stripe/', StripeWebhook.as_view(), name='stripe-webhook'),
    path('success/', SuccessPaymentView.as_view(), name='success-payment'),
    path('failed/', FailedPaymentView.as_view(), name='success-payment'),
]

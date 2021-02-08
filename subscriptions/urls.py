from django.urls import path, include
from .views.stripe import StripeWebhook

app_name = 'subscriptions'

urlpatterns = [
    path('stripe', StripeWebhook.as_view(), name='stripe-webhook')
]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from subscriptions.lib.StripeOperator import StripeOperator
from datetime import datetime, timedelta

from ..lib.PaymentService import PaymentService
from ..models import UserSubscription
from ..documents import documents


class StripeWebhook(APIView):
    def post(self, request, format=None):
        data = request.data
        event = data['type']
        payload = data['data']['object']

        if event == 'checkout.session.completed':
            customer = payload.get('customer', {})
            subscription_id = payload.get('subscription')

            subscription = UserSubscription.objects.filter(
                client_id=customer).first()

            if not subscription:
                return Response(data={'message': 'Customer was not found'}, status=status.HTTP_404_NOT_FOUND)

            subscription.subscription_id = subscription_id
            subscription.subscribed_until = datetime.now() + timedelta(days=35)
            subscription.save()

            return Response(data={'message': 'User subscription created'})

        if event == 'invoice.paid':
            subscription_id = payload.get('subscription')

            if not subscription_id:
                return Response(data={'message': 'Only subscription invoices are supported'}, status=status.HTTP_400_BAD_REQUEST)

            subscription = UserSubscription.objects.filter(
                subscription_id=subscription_id).first()

            if not subscription:
                return Response(data={'message': 'Subscription was not found'}, status=status.HTTP_404_NOT_FOUND)

            subscription.subscribed_until = datetime.now() + timedelta(days=35)
            subscription.save()

            document = documents.PaymentInvoiceDocument(
                user=subscription.user, subscription=subscription)
            document.send()

            return Response(data={'message': 'User subscription refreshed'})

        return Response(data={'message': 'This event is not supported by us but was received'})


class StripeActions(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response(data=StripeOperator().createCheckoutSession(request.user))


class StripeSubscriptions(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, format=None):
        PaymentService(StripeOperator()).cancelSubscription(request.user)
        return Response(data={'message': 'Subscription cancelled'})

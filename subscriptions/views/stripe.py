import sys
from pprint import pprint
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from ..models import UserSubscription


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

            return Response(data={'message': 'User subscription refreshed'})

        return Response(data={'message': 'This event is not supported by us but was received'})

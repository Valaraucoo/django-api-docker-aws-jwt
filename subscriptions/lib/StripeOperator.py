import stripe
from .PaymentOperator import PaymentOperator
from users.models import User
from ..models import UserSubscription
from django.conf import settings
from datetime import datetime, timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeOperator(PaymentOperator):
    def createCustomer(self, user: User) -> None:
        subscription = UserSubscription(user=user)
        customer = stripe.Customer.create(
            description=user.email,
        )
        subscription.client_id = customer['id']
        subscription.save()
        user.subscription = subscription
        user.save()

    def cancelSubscription(self, user: User):
        subscription = user.subscription

        if subscription.subscription_id:
            stripe.Subscription.delete(subscription.subscription_id)

        subscription.subscription_id = None
        subscription.save()

    def createCheckoutSession(self, user: User):
        session = stripe.checkout.Session.create(
            success_url='http://wozniak-dev-api.herokuapp.com/api/subscriptions/success/',
            cancel_url='http://wozniak-dev-api.herokuapp.com/api/subscriptions/failed/',
            payment_method_types=["card"],
            line_items=[
                {"price": 'price_1IIHf8KmDbuO5ZNDHGD75ySO', "quantity": 1}
            ],
            mode="subscription",
            customer=user.subscription.client_id
        )

        return session.id

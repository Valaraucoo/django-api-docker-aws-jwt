from .PaymentOperator import PaymentOperator
from users.models import User


class PaymentService:
    operator: PaymentOperator = None

    def __init__(self, operator: PaymentOperator):
        self.operator = operator

    def createCustomer(self, user: User) -> None:
        self.operator.createCustomer(user)

    def cancelSubscription(self, user: User):
        self.operator.cancelSubscription(user)

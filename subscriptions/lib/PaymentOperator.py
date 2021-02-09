import abc

from users.models import User


class PaymentOperator(abc.ABC):
    @abc.abstractmethod
    def createCustomer(self, user: User):
        pass

    @abc.abstractmethod
    def cancelSubscription(self, user: User):
        pass

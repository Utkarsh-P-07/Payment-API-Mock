import uuid
import stripe
from types import SimpleNamespace
from app.config import STRIPE_SECRET_KEY, is_mock_mode

def _mock_intent(amount, currency):
    return SimpleNamespace(
        id=f"pi_{uuid.uuid4().hex}",
        client_secret=f"secret_{uuid.uuid4().hex}",
        amount=amount,
        currency=currency,
        status="requires_payment_method"
    )

def _mock_refund():
    return SimpleNamespace(
        id=f"re_{uuid.uuid4().hex}",
        status="succeeded"
    )

class StripeService:

    @staticmethod
    def create_payment_intent(amount, currency):
        if is_mock_mode():
            return _mock_intent(amount, currency)

        stripe.api_key = STRIPE_SECRET_KEY
        return stripe.PaymentIntent.create(amount=amount, currency=currency)

    @staticmethod
    def refund_payment(payment_intent_id, reason):
        if is_mock_mode():
            return _mock_refund()

        stripe.api_key = STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.retrieve(payment_intent_id, expand=["charges"])
        charge_id = intent["charges"]["data"][0]["id"]
        return stripe.Refund.create(charge=charge_id, reason=reason)

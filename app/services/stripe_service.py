import uuid
import stripe
from types import SimpleNamespace
from app.config import STRIPE_SECRET_KEY, is_mock_mode
from app.services.mongo_service import MongoService

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

        if not STRIPE_SECRET_KEY:
            raise ValueError("STRIPE_SECRET_KEY is required for live mode")
        
        # Pass api_key directly to avoid thread-safety issues with global stripe.api_key
        return stripe.PaymentIntent.create(amount=amount, currency=currency, api_key=STRIPE_SECRET_KEY)

    @staticmethod
    def refund_payment(payment_intent_id, reason):
        if is_mock_mode():
            # In mock mode, validate that the payment intent exists in the database
            payment_intent = MongoService.get_payment_intent(payment_intent_id)
            if not payment_intent:
                raise ValueError(f"Payment intent {payment_intent_id} not found")
            return _mock_refund()

        if not STRIPE_SECRET_KEY:
            raise ValueError("STRIPE_SECRET_KEY is required for live mode")
        
        # Pass api_key directly to avoid thread-safety issues with global stripe.api_key
        intent = stripe.PaymentIntent.retrieve(payment_intent_id, expand=["charges"], api_key=STRIPE_SECRET_KEY)
        
        # Validate charges data exists and is not empty
        # Stripe objects support both attribute and dict-like access
        charges = getattr(intent, "charges", None)
        if not charges:
            # Try dict-like access as fallback
            try:
                charges = intent["charges"]
            except (KeyError, TypeError):
                charges = None
        
        if not charges:
            raise ValueError(f"No charges found for payment intent {payment_intent_id}")
        
        # Access charges.data safely
        charges_data = getattr(charges, "data", None)
        if not charges_data:
            try:
                charges_data = charges["data"]
            except (KeyError, TypeError):
                charges_data = None
        
        if not charges_data or len(charges_data) == 0:
            raise ValueError(f"No charges found for payment intent {payment_intent_id}")
        
        # Get charge_id from first charge
        first_charge = charges_data[0]
        charge_id = getattr(first_charge, "id", None)
        if not charge_id:
            try:
                charge_id = first_charge["id"]
            except (KeyError, TypeError):
                raise ValueError(f"Charge ID not found for payment intent {payment_intent_id}")
        
        # Pass api_key directly to avoid thread-safety issues with global stripe.api_key
        return stripe.Refund.create(charge=charge_id, reason=reason, api_key=STRIPE_SECRET_KEY)

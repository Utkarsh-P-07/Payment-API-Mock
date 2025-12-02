import stripe
from app.config import STRIPE_SECRET_KEY
from app.utils.logger import logger
from typing import Literal

stripe.api_key = STRIPE_SECRET_KEY


class StripeService:

    @staticmethod
    def create_payment_intent(amount: int, currency: str):
        logger.info(f"Creating PaymentIntent for {amount} {currency}")
        return stripe.PaymentIntent.create(
            amount=amount,
            currency=currency
        )
    
    @staticmethod
    def refund_payment(
        payment_intent_id: str,
        reason: Literal["duplicate", "fraudulent", "requested_by_customer"] = "requested_by_customer"
    ):
        logger.info(f"Refund requested for PaymentIntent: {payment_intent_id}")

        payment_intent = stripe.PaymentIntent.retrieve(
            payment_intent_id,
            expand=["charges"]
        )

        charges = payment_intent.get("charges", {}).get("data", [])
        if not charges:
            raise Exception("No charges found for this PaymentIntent")

        charge_id = charges[0]["id"]

        return stripe.Refund.create(
            charge=charge_id,
            reason=reason
        )

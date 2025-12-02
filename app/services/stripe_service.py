import uuid
from types import SimpleNamespace
from typing import Literal

import stripe

from app.config import STRIPE_SECRET_KEY, is_mock_mode
from app.utils.logger import logger


def _mock_client_secret() -> str:
    return f"pi_{uuid.uuid4().hex}_secret_{uuid.uuid4().hex}"


def _mock_refund_id() -> str:
    return f"re_{uuid.uuid4().hex}"


class StripeService:

    @staticmethod
    def _ensure_live_key():
        if not STRIPE_SECRET_KEY:
            raise ValueError("STRIPE_SECRET_KEY is not configured for live mode.")
        stripe.api_key = STRIPE_SECRET_KEY

    @staticmethod
    def create_payment_intent(amount: int, currency: str):
        logger.info(f"Creating PaymentIntent for {amount} {currency}")

        if is_mock_mode():
            logger.debug("StripeService running in mock mode for PaymentIntent.")
            return SimpleNamespace(client_secret=_mock_client_secret())

        StripeService._ensure_live_key()
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

        if is_mock_mode():
            logger.debug("StripeService running in mock mode for Refund.")
            return SimpleNamespace(id=_mock_refund_id(), status="succeeded")

        StripeService._ensure_live_key()
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

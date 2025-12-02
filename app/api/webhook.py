import json

import stripe
from fastapi import APIRouter, HTTPException, Request

from app.config import STRIPE_WEBHOOK_SECRET, is_mock_mode
from app.utils.logger import logger

router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.post("")
async def stripe_webhook(request: Request):
    payload_bytes = await request.body()
    payload = payload_bytes.decode("utf-8") if payload_bytes else "{}"

    if is_mock_mode():
        logger.debug("Webhook handler running in mock mode; skipping signature validation.")
        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            event = {}
        logger.info(f"Mock webhook received payload: {event}")
        return {"status": "ok"}

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")

    sig_header = request.headers.get("stripe-signature")
    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    logger.info(f"Webhook received: {event['type']}")

    if event["type"] == "payment_intent.succeeded":
        logger.info("Payment SUCCEEDED")

    return {"status": "ok"}

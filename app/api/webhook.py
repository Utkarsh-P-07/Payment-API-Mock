import json
import stripe
from fastapi import APIRouter, Request, HTTPException

from app.config import STRIPE_WEBHOOK_SECRET, is_mock_mode
from app.utils.logger import logger

router = APIRouter(prefix="/webhook", tags=["Webhook"])

@router.post("")
async def stripe_webhook(request: Request):
    payload = (await request.body()).decode("utf-8")

    if is_mock_mode():
        logger.info("Mock mode — ignoring signature.")
        return {"status": "ok"}

    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except:
        raise HTTPException(status_code=400, detail="Invalid signature")

    logger.info(f"Webhook event received: {event['type']}")

    return {"status": "ok"}

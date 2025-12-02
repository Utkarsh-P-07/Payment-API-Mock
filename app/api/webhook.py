from fastapi import APIRouter, Request, HTTPException
import stripe
from app.config import STRIPE_WEBHOOK_SECRET
from app.utils.logger import logger

router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.post("")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    logger.info(f"Webhook received: {event['type']}")

    if event["type"] == "payment_intent.succeeded":
        logger.info("Payment SUCCEEDED")

    return {"status": "ok"}

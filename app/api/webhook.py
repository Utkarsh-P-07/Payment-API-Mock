import stripe
from fastapi import APIRouter, Request, HTTPException

from app.config import STRIPE_WEBHOOK_SECRET, is_mock_mode
from app.utils.logger import logger

router = APIRouter(prefix="/webhook", tags=["Webhook"])

@router.post("")
async def stripe_webhook(request: Request):
    try:
        payload = (await request.body()).decode("utf-8")
    except UnicodeDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid payload encoding: {str(e)}")

    if is_mock_mode():
        logger.info("Mock mode — ignoring signature.")
        return {"status": "ok"}

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=500, 
            detail="STRIPE_WEBHOOK_SECRET is required for webhook verification in live mode"
        )

    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid signature: {str(e)}")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid signature: {str(e)}")

    # Safely access event type
    event_type = event.get("type") if isinstance(event, dict) else getattr(event, "type", "unknown")
    logger.info(f"Webhook event received: {event_type}")

    return {"status": "ok"}

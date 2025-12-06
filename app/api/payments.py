from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

from app.config import is_mock_mode
from app.schemas.payments import PaymentIntentRequest
from app.services.mongo_service import MongoService
from app.services.stripe_service import StripeService

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/create-intent")
def create_intent(payload: PaymentIntentRequest):
    try:
        intent = StripeService.create_payment_intent(
            amount=payload.amount,
            currency=payload.currency
        )

        client_secret = getattr(intent, "client_secret", None)
        intent_id = getattr(intent, "id", None)

        MongoService.record_payment_intent({
            "payment_intent_id": intent_id,
            "amount": payload.amount,
            "currency": payload.currency,
            "status": getattr(intent, "status", "created"),
            "client_secret": client_secret,
            "mode": "mock" if is_mock_mode() else "live",
            "created_at": datetime.now(timezone.utc),
        })

        return {"client_secret": client_secret}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

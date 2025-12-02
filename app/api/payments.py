from fastapi import APIRouter, HTTPException
from app.schemas.payments import PaymentIntentRequest
from app.services.stripe_service import StripeService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create-intent")
def create_intent(payload: PaymentIntentRequest):
    try:
        intent = StripeService.create_payment_intent(
            amount=payload.amount,
            currency=payload.currency
        )
        return {"client_secret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter, HTTPException
from app.schemas.refund import RefundRequest
from app.services.stripe_service import StripeService

router = APIRouter(prefix="/refund", tags=["Refund"])

@router.post("")
def refund(payload: RefundRequest):
    try:
        return StripeService.refund_payment(
            payment_intent_id=payload.payment_intent_id,
            reason=payload.reason
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

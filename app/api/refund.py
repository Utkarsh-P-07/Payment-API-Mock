from fastapi import APIRouter, HTTPException
import stripe
from app.schemas.refund import RefundRequest
from app.services.stripe_service import StripeService

router = APIRouter(prefix="/refund", tags=["Refund"])

@router.post("")
def refund(payload: RefundRequest):
    # Validate payment_intent_id format (Stripe payment intent IDs start with 'pi_')
    if not payload.payment_intent_id or not payload.payment_intent_id.startswith("pi_"):
        raise HTTPException(
            status_code=400, 
            detail="Invalid payment_intent_id format. Must start with 'pi_'"
        )
    
    try:
        refund_result = StripeService.refund_payment(
            payment_intent_id=payload.payment_intent_id,
            reason=payload.reason
        )
        
        # Convert Stripe object or SimpleNamespace to dict for proper JSON serialization
        refund_id = getattr(refund_result, "id", None)
        refund_status = getattr(refund_result, "status", None)
        
        if not refund_id:
            raise HTTPException(status_code=500, detail="Refund creation failed: missing refund ID")
        
        return {
            "refund_id": refund_id,
            "status": refund_status,
            "payment_intent_id": payload.payment_intent_id
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refund failed: {str(e)}")

from fastapi import APIRouter, HTTPException
import stripe
from app.schemas.refund import RefundRequest
from app.services.stripe_service import StripeService

router = APIRouter(prefix="/refund", tags=["Refund"])

@router.post("")
def refund(payload: RefundRequest):
    # Validation is now handled by Pydantic schema
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
    except HTTPException:
        # Re-raise HTTPException to let FastAPI handle it
        raise
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except ValueError as e:
        # Check if it's a "not found" error
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refund failed: {str(e)}")

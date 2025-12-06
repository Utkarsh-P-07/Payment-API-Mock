from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
import stripe

from app.config import is_mock_mode
from app.schemas.payments import PaymentIntentRequest
from app.services.mongo_service import MongoService
from app.services.stripe_service import StripeService

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/create-intent")
def create_intent(payload: PaymentIntentRequest):
    intent = None
    try:
        intent = StripeService.create_payment_intent(
            amount=payload.amount,
            currency=payload.currency
        )

        client_secret = getattr(intent, "client_secret", None)
        intent_id = getattr(intent, "id", None)

        # Validate that intent was created successfully
        if not intent_id:
            raise HTTPException(status_code=500, detail="Payment intent creation failed: missing intent ID")
        if not client_secret:
            raise HTTPException(status_code=500, detail="Payment intent creation failed: missing client secret")

        try:
            MongoService.record_payment_intent({
                "payment_intent_id": intent_id,
                "amount": payload.amount,
                "currency": payload.currency,
                "payer_name": payload.payer_name,
                "status": getattr(intent, "status", "created"),
                "client_secret": client_secret,
                "mode": "mock" if is_mock_mode() else "live",
                "created_at": datetime.now(timezone.utc),
            })
        except Exception as db_error:
            # Log the database error but still return the payment intent
            # This prevents losing the payment intent if DB write fails
            from app.utils.logger import logger
            logger.error(f"Failed to record payment intent {intent_id} to database: {str(db_error)}")
            # Continue execution - payment intent was created successfully

        return {"client_secret": client_secret}

    except HTTPException:
        # Re-raise HTTPException to let FastAPI handle it
        raise
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

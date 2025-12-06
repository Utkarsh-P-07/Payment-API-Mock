from pydantic import BaseModel, Field, field_validator
from typing import Literal

class RefundRequest(BaseModel):
    payment_intent_id: str = Field(
        ...,
        min_length=3,
        description="Stripe payment intent ID (must start with 'pi_')",
        examples=["pi_1234567890abcdef"]
    )
    reason: Literal["duplicate", "fraudulent", "requested_by_customer"] = "requested_by_customer"
    
    @field_validator('payment_intent_id')
    @classmethod
    def validate_payment_intent_id(cls, v: str) -> str:
        if not v or not v.startswith("pi_"):
            raise ValueError("payment_intent_id must start with 'pi_' (e.g., 'pi_1234567890abcdef')")
        if len(v) < 10:  # Minimum reasonable length for a Stripe ID
            raise ValueError("payment_intent_id appears to be too short")
        return v

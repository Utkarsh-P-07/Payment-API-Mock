from pydantic import BaseModel, Field

class PaymentIntentRequest(BaseModel):
    amount: int = Field(..., gt=0)
    currency: str = "inr"
    payer_name: str = Field(..., min_length=1)

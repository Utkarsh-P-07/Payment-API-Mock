from pydantic import BaseModel, Field

class PaymentIntentRequest(BaseModel):
    amount: int = Field(..., gt=0)
    currency: str = "usd"

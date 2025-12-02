from pydantic import BaseModel, Field

class PaymentIntentRequest(BaseModel):
    amount: int = Field(..., gt=0, description="Amount in cents")
    currency: str = "usd"

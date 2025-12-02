from pydantic import BaseModel
from typing import Literal

RefundReason = Literal["duplicate", "fraudulent", "requested_by_customer"]

class RefundRequest(BaseModel):
    payment_intent_id: str
    reason: RefundReason = "requested_by_customer"

from pydantic import BaseModel
from typing import Literal

class RefundRequest(BaseModel):
    payment_intent_id: str
    reason: Literal["duplicate", "fraudulent", "requested_by_customer"] = "requested_by_customer"

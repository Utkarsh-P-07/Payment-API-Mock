from fastapi import FastAPI
from app.api import payments, webhook, refund

app = FastAPI(title="Payment API Mock (Stripe Sandbox)")

app.include_router(payments.router)
app.include_router(webhook.router)
app.include_router(refund.router)


@app.get("/")
def root():
    return {"message": "Payment API Mock Running"}

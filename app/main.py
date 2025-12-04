import base64

from fastapi import FastAPI
from fastapi.responses import Response

from app.api import payments, refund, webhook

app = FastAPI(title="Payment API Mock (Stripe Sandbox)")

app.include_router(payments.router)
app.include_router(webhook.router)
app.include_router(refund.router)

_FAVICON_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/"
    "PvWSWQAAAABJRU5ErkJggg=="
)


@app.get("/")
def root():
    return {"message": "Payment API Mock Running"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(content=_FAVICON_PNG, media_type="image/png")

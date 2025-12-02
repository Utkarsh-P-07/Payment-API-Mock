import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_payment_intent(mock_stripe_payment_intent_create):
    payload = {"amount": 1000, "currency": "usd"}

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/payments/create-intent", json=payload)

    assert resp.status_code == 200
    assert "client_secret" in resp.json()

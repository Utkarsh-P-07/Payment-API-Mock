import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_webhook_invalid_signature():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/webhook",
            content=b"{}",
            headers={"stripe-signature": "invalid"}
        )

    assert resp.status_code == 400

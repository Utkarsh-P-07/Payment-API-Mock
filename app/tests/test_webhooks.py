import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_webhook_invalid_signature(monkeypatch):
    monkeypatch.setattr("app.api.webhook.is_mock_mode", lambda: False)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/webhook",
            content=b"{}",
            headers={"stripe-signature": "invalid"}
        )

    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_webhook_mock_mode_skips_signature(monkeypatch):
    monkeypatch.setattr("app.api.webhook.is_mock_mode", lambda: True)
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/webhook", content=b"{}")

    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

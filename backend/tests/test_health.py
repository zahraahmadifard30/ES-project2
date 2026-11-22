import pytest


@pytest.mark.asyncio
async def test_health_live_returns_ok(client):
    response = await client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

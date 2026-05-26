import pytest


@pytest.mark.asyncio
async def test_remove_participant_success(async_client):
    # Arrange
    activity = "Chess Club"
    # use an existing participant from the initial data
    email = "michael@mergington.edu"

    # Act
    resp = await async_client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")

    # verify participant removed
    get_resp = await async_client.get("/activities")
    assert email not in get_resp.json()[activity]["participants"]


@pytest.mark.asyncio
async def test_remove_nonexistent_activity(async_client):
    # Arrange
    activity = "Unknown Club"
    email = "someone@mergington.edu"

    # Act
    resp = await async_client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "").lower()


@pytest.mark.asyncio
async def test_remove_nonexistent_participant(async_client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    resp = await async_client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "").lower()

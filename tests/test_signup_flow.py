import pytest


@pytest.mark.asyncio
async def test_signup_success(async_client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    resp = await async_client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")

    # verify participant added
    get_resp = await async_client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]


@pytest.mark.asyncio
async def test_signup_duplicate(async_client):
    # Arrange
    activity = "Chess Club"
    email = "duplicate@mergington.edu"

    # sign up first time
    first = await async_client.post(f"/activities/{activity}/signup", params={"email": email})
    assert first.status_code == 200

    # Act - sign up second time
    second = await async_client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert second.status_code == 400
    assert "already" in second.json().get("detail", "").lower()


@pytest.mark.asyncio
async def test_signup_unknown_activity(async_client):
    # Arrange
    activity = "Nonexistent Club"
    email = "nobody@mergington.edu"

    # Act
    resp = await async_client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "").lower()

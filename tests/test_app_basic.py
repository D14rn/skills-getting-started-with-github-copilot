import pytest

@pytest.mark.asyncio
async def test_root_redirect(async_client):
    # Arrange
    # Act
    response = await async_client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


@pytest.mark.asyncio
async def test_get_activities(async_client):
    # Arrange
    # Act
    response = await async_client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    # verify expected keys exist for one activity
    activity = data["Chess Club"]
    assert "participants" in activity
    assert "description" in activity

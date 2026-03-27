import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Users tests
# ---------------------------------------------------------------------------

def test_get_users_returns_list():
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_users_have_required_fields():
    response = client.get("/users")
    for user in response.json():
        assert "id" in user
        assert "name" in user
        assert "email" in user
        assert "city" in user


def test_get_user_by_id():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice Johnson"


def test_get_user_not_found():
    response = client.get("/users/9999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Weather tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("city", ["austin", "new york", "geneva"])
def test_get_weather_supported_cities(city):
    response = client.get(f"/weather/{city}")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert "country" in data
    assert "readings" in data
    assert len(data["readings"]) > 0


def test_get_weather_readings_have_required_fields():
    response = client.get("/weather/austin")
    for reading in response.json()["readings"]:
        assert "date" in reading
        assert "temperature_c" in reading
        assert "humidity_pct" in reading


def test_get_weather_dates_are_2026():
    for city in ["austin", "new york", "geneva"]:
        response = client.get(f"/weather/{city}")
        for reading in response.json()["readings"]:
            assert reading["date"].startswith("2026"), (
                f"Expected 2026 date, got {reading['date']} for {city}"
            )


def test_get_weather_unsupported_city():
    response = client.get("/weather/london")
    assert response.status_code == 404


def test_get_weather_case_insensitive():
    response = client.get("/weather/Austin")
    assert response.status_code == 200
    assert response.json()["city"] == "Austin"

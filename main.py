from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="My API", version="1.0.0")


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

class User(BaseModel):
    id: int
    name: str
    email: str
    city: str


USERS: list[User] = [
    User(id=1, name="Alice Johnson", email="alice@example.com", city="Austin"),
    User(id=2, name="Bob Smith", email="bob@example.com", city="New York"),
    User(id=3, name="Carol White", email="carol@example.com", city="Geneva"),
    User(id=4, name="David Brown", email="david@example.com", city="Austin"),
    User(id=5, name="Eva Martinez", email="eva@example.com", city="New York"),
]


@app.get("/users", response_model=list[User])
def get_users():
    """Return the full list of fake users."""
    return USERS


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Return a single user by ID."""
    for user in USERS:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


# ---------------------------------------------------------------------------
# Weather
# ---------------------------------------------------------------------------

class WeatherReading(BaseModel):
    date: str
    temperature_c: float
    humidity_pct: int


class CityWeather(BaseModel):
    city: str
    country: str
    readings: list[WeatherReading]


WEATHER: dict[str, CityWeather] = {
    "austin": CityWeather(
        city="Austin",
        country="US",
        readings=[
            WeatherReading(date="2026-03-01", temperature_c=18.5, humidity_pct=55),
            WeatherReading(date="2026-03-08", temperature_c=21.0, humidity_pct=50),
            WeatherReading(date="2026-03-15", temperature_c=24.3, humidity_pct=48),
            WeatherReading(date="2026-03-22", temperature_c=26.1, humidity_pct=45),
            WeatherReading(date="2026-03-29", temperature_c=27.8, humidity_pct=43),
        ],
    ),
    "new york": CityWeather(
        city="New York",
        country="US",
        readings=[
            WeatherReading(date="2026-03-01", temperature_c=4.2, humidity_pct=70),
            WeatherReading(date="2026-03-08", temperature_c=6.5, humidity_pct=68),
            WeatherReading(date="2026-03-15", temperature_c=9.1, humidity_pct=65),
            WeatherReading(date="2026-03-22", temperature_c=11.4, humidity_pct=62),
            WeatherReading(date="2026-03-29", temperature_c=13.7, humidity_pct=60),
        ],
    ),
    "geneva": CityWeather(
        city="Geneva",
        country="CH",
        readings=[
            WeatherReading(date="2026-03-01", temperature_c=6.0, humidity_pct=75),
            WeatherReading(date="2026-03-08", temperature_c=8.3, humidity_pct=72),
            WeatherReading(date="2026-03-15", temperature_c=10.5, humidity_pct=69),
            WeatherReading(date="2026-03-22", temperature_c=12.8, humidity_pct=66),
            WeatherReading(date="2026-03-29", temperature_c=14.0, humidity_pct=63),
        ],
    ),
}

SUPPORTED_CITIES = ", ".join(c.title() for c in WEATHER)


@app.get("/weather/{city}", response_model=CityWeather)
def get_weather(city: str):
    """Return fake weekly weather readings for a supported city.

    Supported cities: Austin, New York, Geneva.
    """
    key = city.lower()
    if key not in WEATHER:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city}' not found. Supported cities: {SUPPORTED_CITIES}.",
        )
    return WEATHER[key]

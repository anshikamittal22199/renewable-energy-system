// ...existing code...
# Renewable Energy System

A small example project that simulates a renewable energy forecasting and grid-balancing system built with Django, Django REST Framework, and Docker Compose.

It contains two lightweight microservices:
- `solar_forecaster` — forecasts solar power generation (kWh) from sunlight intensity and daylight duration.
- `grid_balancer` — consumes forecasts to decide whether to store, use, or sell energy.

---

## Architecture Overview

User → POST /balance/ → `grid_balancer` → (API call) → `solar_forecaster`  
                                   ← forecast_kwh + decision ←  
Docker network: `renewable_net`

---

## Setup and Run

1. Clone the repository
```bash
git clone https://github.com/<your-username>/renewable-energy-system.git
cd renewable-energy-system
```

2. Build and start containers
```bash
docker compose up --build
```

This will start:
- `solar_forecaster` service on port `8001`
- `grid_balancer` service on port `8000`

3. Verify health
```bash
curl http://localhost:8000/health/
curl http://localhost:8001/health/
```

---

## API Endpoints

### Solar Forecaster Service
Base URL: `http://localhost:8001`

| Method | Endpoint    | Description            |
|--------|-------------|------------------------|
| POST   | /forecast/  | Create a solar forecast|
| GET    | /health/    | Check app health       |

Example request (POST /forecast/):
```json
{
  "location": "Gurgaon",
  "date": "2025-11-08",
  "sun_intensity_factor": 5.5,
  "daylight_hours": 10
}
```

Example response:
```json
{
  "location": "Gurgaon",
  "date": "2025-11-08",
  "forecast_kwh": 105.5
}
```

### Grid Balancer Service
Base URL: `http://localhost:8000`

| Method | Endpoint   | Description                          |
|--------|------------|--------------------------------------|
| POST   | /balance/  | Fetch forecast and make a decision   |
| GET    | /health/   | Check app health                     |

Example request (POST /balance/):
```json
{
  "location": "Gurgaon",
  "date": "2025-11-08",
  "sun_intensity_factor": 5.5,
  "daylight_hours": 10
}
```

Example response:
```json
{
  "forecast_kwh": 105.5,
  "decision": "use"
}
```

---

## Decision Logic

| Forecast (kWh)       | Decision |
|----------------------|----------|
| forecast < 50        | store    |
| 50 ≤ forecast < 150  | use      |
| forecast ≥ 150       | sell     |

---

## Project Structure

```
renewable-energy-system/
├── docker-compose.yml
├── solar_forecaster/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── forecast/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── tests.py
│   └── solar_forecaster/
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
└── grid_balancer/
    ├── Dockerfile
    ├── requirements.txt
    ├── balance/
    │   ├── models.py
    │   ├── views.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── tests.py
    └── grid_balancer/
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

---

## Logging

Both services include basic logging. Errors, invalid input, and connection failures are logged to the console with descriptive messages for debugging.

---

## Unit Tests

Each app includes simple tests for:
- Valid forecast creation
- Invalid input handling
- API communication between services

Run tests inside the containers:
```bash
docker compose exec solar_forecaster python manage.py test
docker compose exec grid_balancer python manage.py test
```

---
```// filepath: /workspaces/renewable-energy-system/README.md
// ...existing code...
# Renewable Energy System

A small example project that simulates a renewable energy forecasting and grid-balancing system built with Django, Django REST Framework, and Docker Compose.

It contains two lightweight microservices:
- `solar_forecaster` — forecasts solar power generation (kWh) from sunlight intensity and daylight duration.
- `grid_balancer` — consumes forecasts to decide whether to store, use, or sell energy.

---

## Architecture Overview

User → POST /balance/ → `grid_balancer` → (API call) → `solar_forecaster`  
                                   ← forecast_kwh + decision ←  
Docker network: `renewable_net`

---

## Setup and Run

1. Clone the repository
```bash
git clone https://github.com/<your-username>/renewable-energy-system.git
cd renewable-energy-system
```

2. Build and start containers
```bash
docker compose up --build
```

This will start:
- `solar_forecaster` service on port `8001`
- `grid_balancer` service on port `8000`

3. Verify health
```bash
curl http://localhost:8000/health/
curl http://localhost:8001/health/
```

---

## API Endpoints

### Solar Forecaster Service
Base URL: `http://localhost:8001`

| Method | Endpoint    | Description            |
|--------|-------------|------------------------|
| POST   | /forecast/  | Create a solar forecast|
| GET    | /health/    | Check app health       |

Example request (POST /forecast/):
```json
{
  "location": "Gurgaon",
  "date": "2025-11-08",
  "sun_intensity_factor": 5.5,
  "daylight_hours": 10
}
```

Example response:
```json
{
  "location": "Gurgaon",
  "date": "2025-11-08",
  "forecast_kwh": 105.5
}
```

### Grid Balancer Service
Base URL: `http://localhost:8000`

| Method | Endpoint   | Description                          |
|--------|------------|--------------------------------------|
| POST   | /balance/  | Fetch forecast and make a decision   |
| GET    | /health/   | Check app health                     |

Example request (POST /balance/):
```json
{
  "location": "Gurgaon",
  "date": "2025-11-08",
  "sun_intensity_factor": 5.5,
  "daylight_hours": 10
}
```

Example response:
```json
{
  "forecast_kwh": 105.5,
  "decision": "use"
}
```

---

## Decision Logic

| Forecast (kWh)       | Decision |
|----------------------|----------|
| forecast < 50        | store    |
| 50 ≤ forecast < 150  | use      |
| forecast ≥ 150       | sell     |

---

## Project Structure

```
renewable-energy-system/
├── docker-compose.yml
├── solar_forecaster/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── forecast/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── tests.py
│   └── solar_forecaster/
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
└── grid_balancer/
    ├── Dockerfile
    ├── requirements.txt
    ├── balance/
    │   ├── models.py
    │   ├── views.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── tests.py
    └── grid_balancer/
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

---

## Logging

Both services include basic logging. Errors, invalid input, and connection failures are logged to the console with descriptive messages for debugging.

---

## Unit Tests

Each app includes simple tests for:
- Valid forecast creation
- Invalid input handling
- API communication between services

Run tests inside the containers:
```bash
docker compose exec solar_forecaster python manage.py test
docker compose exec grid_balancer python manage.py test
```

---
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
# Renewable Energy System

This repository contains two small Django microservices that simulate a simplified renewable energy system:

- solar_forecaster — produces simple solar production forecasts (kWh)
- grid_balancer — fetches forecasts and decides whether to store, use, or sell energy

Both services run in separate Docker containers and communicate over a Docker network using REST APIs.

## Quick start (development)

1. Clone the repo and change into it:

```bash
git clone https://github.com/<your-username>/renewable-energy-system.git
cd renewable-energy-system
```

2. Build and start both services (rebuild when you change Dockerfiles):

```bash
docker compose up --build -d
```

By default the project maps container ports to host ports as follows:
- solar_forecaster (container listens on 8000) → host http://localhost:8001
- grid_balancer   (container listens on 8000) → host http://localhost:8002

3. (If needed) run migrations inside the running containers:

```bash
docker compose exec solar_forecaster python manage.py makemigrations forecast
docker compose exec solar_forecaster python manage.py migrate

docker compose exec grid_balancer python manage.py makemigrations
docker compose exec grid_balancer python manage.py migrate
```

Note: the project includes an entrypoint in `solar_forecaster` that attempts to create and apply migrations at container start in development. If you recreate containers after code changes you may still need to run the migrate commands above.

## Health checks

From the host:

```bash
curl http://localhost:8001/health/
curl http://localhost:8002/health/
```

## API: example curl calls

Solar forecaster (host → container)

```bash
curl -sS -X POST http://localhost:8001/forecast/ \
  -H "Content-Type: application/json" \
  -d '{"location":"Gurgaon","date":"2025-11-08","sun_intensity_factor":5.5,"daylight_hours":10}'
```

Grid balancer (host → container)

```bash
curl -sS -X POST http://localhost:8002/balance/ \
  -H "Content-Type: application/json" \
  -d '{"location":"Gurgaon","date":"2025-11-08","sun_intensity_factor":5.5,"daylight_hours":10}'
```

If you need to debug inter-container networking (grid_balancer calling solar_forecaster), you can run the same requests from inside either container. Example (from grid_balancer):

```bash
docker compose exec grid_balancer curl -v -X POST http://solar-forecaster:8000/forecast/ \
  -H "Content-Type: application/json" \
  -d '{"location":"Gurgaon","date":"2025-11-08","sun_intensity_factor":5.5,"daylight_hours":10}'
```

Important: host port vs container port
- Services are reachable from your host at the host ports listed above (8001, 8002).
- From one container to another (inter-container) use the container port (8000) and the service name or network alias. The grid_balancer uses an environment variable to configure the forecaster URL and the compose setup provides a network alias `solar-forecaster` (no underscore) for the forecaster container to avoid Django host validation errors.

## Why the environment variable

The grid_balancer fetches forecasts from the forecaster using the URL in an environment variable `SOLAR_FORECASTER_URL`. This allows you to test locally (host access) or rely on the internal Docker network when services call one another.

The default used in code is `http://solar-forecaster:8000/forecast/` and `docker-compose.yml` sets the same value for the `grid_balancer` service.

## Updating code and picking up changes

- Development (fast feedback): the `docker-compose.yml` bind-mounts each service's source into the container (e.g. `./solar_forecaster:/app`). Edit files locally and the Django dev server will auto-reload. If the running process doesn't pick up a change, restart just that service:

```bash
docker compose restart grid_balancer
```

- When changing Dockerfiles or dependencies, rebuild the image and recreate the container:

```bash
docker compose build grid_balancer
docker compose up -d --force-recreate grid_balancer
```

## Decision logic

The grid balancer implements a simple rule:

- forecast_kwh < 50  → store
- 50 ≤ forecast_kwh < 150 → use
- forecast_kwh ≥ 150 → sell

## Troubleshooting

- "no such table: forecast_forecast": run migrations (see commands above) inside the running `solar_forecaster` container.
- "solar_forecaster service unavailable": confirm `SOLAR_FORECASTER_URL` in `docker-compose.yml` (grid_balancer) and test connectivity from inside `grid_balancer` with curl (see example above).
- "Bad Request (400)" with a Django DisallowedHost error: ensure the hostname used by the request does not contain underscores. This repo uses the network alias `solar-forecaster` (no underscore) to avoid that.

## Project structure

```
renewable-energy-system/
├── docker-compose.yml
├── solar_forecaster/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── requirements.txt
│   └── forecast/
├── grid_balancer/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── balance/
└── README.md
```

## Tests

Run the Django tests inside the running containers:

```bash
docker compose exec solar_forecaster python manage.py test
docker compose exec grid_balancer python manage.py test
```

---

If you'd like, I can also add a short development README in each service folder, wire up a named volume for persistent sqlite storage, or switch the project to a Postgres service for production-like persistence. Let me know which you prefer.

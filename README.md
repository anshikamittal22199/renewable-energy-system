# Renewable Energy System

This project simulates a renewable energy forecasting and grid balancing system built using Django, Django REST Framework, and Docker Compose.

It consists of two lightweight microservices:
- solar_forecaster — forecasts solar power generation (kWh) based on sunlight intensity and daylight duration.
- grid_balancer — consumes forecasts from the forecaster to decide whether to store, use, or sell energy.

---

## Architecture Overview

User → POST /balance/ → grid_balancer → (API call) → solar_forecaster  
                                   ← forecast_kwh + decision ←  
Docker Network (renewable_net)

---

## Setup and Run

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/renewable-energy-system.git
cd renewable-energy-system

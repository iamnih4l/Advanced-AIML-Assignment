# Backend API Documentation

This document describes the FastAPI backend service built for the Semiconductor Manufacturing Defect Prediction system. The API serves the serialized ML pipeline from Milestone 3 and enforces strict data validation.

## Architecture & Framework
- **Framework**: FastAPI (Python)
- **Validation**: Pydantic for strong typing and bounding of process parameters.
- **Model Lifecycle**: The ML Pipeline is loaded exactly once into memory during the application's `lifespan` startup event, preventing the heavy cost of reloading the model on every inference request.

## Endpoints

### 1. `GET /health`
Used by load balancers and monitors to verify the service is running and the ML model is successfully loaded into memory.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 2. `POST /predict`
The core inference endpoint. It accepts a JSON payload of manufacturing parameters, passes them through the serialized preprocessing pipeline (imputation, engineering, scaling, encoding), and returns the prediction and risk classification.

**Risk Classification Logic:**
- **LOW**: Defect probability < 20%
- **MEDIUM**: Defect probability 20% - 49.9%
- **HIGH**: Defect probability >= 50%

**Example Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "chamber_temperature": 205.5,
  "chamber_pressure": 5.2,
  "gas_flow_rate": 102.0,
  "deposition_time": 30.5,
  "plasma_power": 510.0,
  "process_voltage": 225.0,
  "process_current": 15.2,
  "equipment_id": "CHAMBER-01",
  "equipment_age": 5.5,
  "vibration_level": 1.2,
  "sensor_health_score": 85.0,
  "maintenance_days_since": 30,
  "machine_utilization": 0.8,
  "ambient_temperature": 22.5,
  "ambient_humidity": 45.0,
  "cleanroom_temperature": 21.0,
  "cleanroom_humidity": 40.0,
  "wafer_type": "TYPE_A",
  "material_type": "SILICON",
  "process_recipe": "RECIPE_1",
  "production_shift": "MORNING",
  "operator_shift": "TEAM_ALPHA",
  "production_line": "LINE_1",
  "recent_maintenance_flag": 0,
  "machine_failure_count": 1,
  "previous_batch_defects": 2
}'
```

**Example Response:**
```json
{
  "prediction": 0,
  "defect_probability": 0.1245,
  "risk_level": "LOW",
  "model_version": "LogisticRegression-Pipeline-v1"
}
```

## Running the API Locally

From the root directory of the repository:
```bash
uvicorn backend.app.main:app --reload --port 8000
```
Then visit `http://localhost:8000/docs` to view the interactive Swagger UI.

## Automated Testing
Automated testing is implemented using `pytest` and FastAPI's `TestClient`. Six tests ensure that valid payloads succeed, invalid schemas are rejected with standard HTTP 422 errors, probability bounds are enforced, and the health endpoint functions correctly.

Run the tests using:
```bash
python -m pytest backend/tests/
```

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

valid_payload = {
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
}

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] == True

def test_valid_prediction(client):
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] in [0, 1]
    assert "defect_probability" in data
    assert 0.0 <= data["defect_probability"] <= 1.0
    assert "risk_level" in data
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
    assert "model_version" in data

def test_missing_required_field(client):
    invalid_payload = valid_payload.copy()
    del invalid_payload["chamber_temperature"]
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422 # Unprocessable Entity
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "chamber_temperature"]

def test_invalid_numerical_type(client):
    invalid_payload = valid_payload.copy()
    invalid_payload["chamber_pressure"] = "invalid_string_not_a_float"
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["type"] in ["type_error.float", "float_parsing"]

def test_invalid_value_range(client):
    invalid_payload = valid_payload.copy()
    # machine_utilization is constrained between 0.0 and 1.0
    invalid_payload["machine_utilization"] = 2.5 
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422
    data = response.json()
    # Pydantic will raise a less_than_equal error
    assert data["detail"][0]["type"] == "less_than_equal"

def test_probability_and_risk_thresholds(client):
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    prob = data["defect_probability"]
    risk = data["risk_level"]
    
    if prob < 0.20:
        assert risk == "LOW"
    elif prob < 0.50:
        assert risk == "MEDIUM"
    else:
        assert risk == "HIGH"

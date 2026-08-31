import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.utils import calculate_haversine_distance, is_within_geofence

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_login_success():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "luis@correo.com", "password": "123456"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["correo"] == "luis@correo.com"

def test_list_actividades():
    response = client.get("/api/v1/actividades")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3

def test_geofencing_haversine_validation():
    # Punto en Bogotá
    lat1, lon1 = 4.711000, -74.072100
    # Punto a ~22 metros
    lat2, lon2 = 4.711200, -74.072100

    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    assert distance < 50

    is_inside = is_within_geofence(lat1, lon1, lat2, lon2, radius_meters=100)
    assert is_inside is True

def test_check_in_asistencia():
    payload = {
        "actividad_id": "act-001",
        "usuario_id": "a1010000-0000-0000-0000-000000000001",
        "lat_registrada": 4.711100,
        "lng_registrada": -74.072100,
        "distancia_metros": 15,
        "precision_gps": "Alta"
    }
    response = client.post("/api/v1/asistencias", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["actividad_id"] == "act-001"
    assert data["precision_gps"] == "Alta"

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_expected_response():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["x-request-id"]


def test_work_endpoint_returns_expected_response():
    response = client.get("/work")

    assert response.status_code == 200
    assert response.json() == {
        "status": "completed",
        "result": "simulated work",
    }
    assert response.headers["x-request-id"]

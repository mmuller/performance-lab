from fastapi.testclient import TestClient

from app.main import WORK_CAPACITY_LIMIT, WORK_PROCESSING_DELAY_MS, app


client = TestClient(app)


def test_health_endpoint_returns_expected_response():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["x-request-id"]


def test_work_endpoint_returns_expected_response():
    request_id = "smoke-test-request"
    response = client.get("/work", headers={"x-request-id": request_id})
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "completed"
    assert body["request_id"] == request_id
    assert body["processing_delay_ms"] == WORK_PROCESSING_DELAY_MS
    assert 1 <= body["active_requests"] <= body["capacity_limit"]
    assert body["capacity_limit"] == WORK_CAPACITY_LIMIT
    assert response.headers["x-request-id"] == request_id

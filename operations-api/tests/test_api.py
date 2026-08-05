from fastapi.testclient import TestClient

from app.main import app, jobs

client = TestClient(app)


def setup_function() -> None:
    jobs.clear()


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_job() -> None:
    created = client.post(
        "/jobs",
        json={"title": "Prepare weekly report", "owner": "Usman", "priority": "high"},
    )
    assert created.status_code == 201
    assert created.json()["status"] == "pending"

    listed = client.get("/jobs")
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_update_unknown_job_returns_404() -> None:
    response = client.patch("/jobs/999/status", params={"status": "completed"})
    assert response.status_code == 404

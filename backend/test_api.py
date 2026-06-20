"""API integration tests for ResumeIQ."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_list_roles():
    response = client.get("/roles")
    assert response.status_code == 200
    roles = response.json()["roles"]
    assert "Software Engineer" in roles
    assert "AI Engineer" in roles


def test_demo_endpoint():
    response = client.get("/demo")
    assert response.status_code == 200
    body = response.json()
    assert "ats_score" in body
    assert "skill_evidence" in body
    assert "interview_questions" in body


def test_upload_rejects_non_pdf():
    response = client.post(
        "/upload-resume",
        files={"file": ("resume.txt", b"not a pdf", "text/plain")},
        data={"role": "Software Engineer"},
    )
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_upload_rejects_invalid_role():
    response = client.post(
        "/upload-resume",
        files={"file": ("resume.pdf", b"%PDF-1.4 fake", "application/pdf")},
        data={"role": "Invalid Role"},
    )
    assert response.status_code == 400


def test_ai_coach():
    response = client.post(
        "/ai-coach",
        json={"question": "How does ResumeIQ scoring work?", "role": "Software Engineer"},
    )
    assert response.status_code == 200
    answer = response.json()["answer"]
    assert isinstance(answer, str)
    assert len(answer) > 20


def test_ai_coach_rejects_invalid_role():
    response = client.post(
        "/ai-coach",
        json={"question": "Hello", "role": "Invalid Role"},
    )
    assert response.status_code == 400

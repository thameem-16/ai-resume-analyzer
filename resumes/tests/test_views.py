import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_register_creates_user_and_returns_token(client):
    response = client.post("/api/auth/register/", {
        "username": "newuser",
        "password": "SecurePass123!",
        "email": "newuser@example.com",
    }, content_type="application/json")

    assert response.status_code == 201
    assert "token" in response.json()


@pytest.mark.django_db
def test_register_duplicate_username_fails(client, test_user):
    response = client.post("/api/auth/register/", {
        "username": "testuser",  # already exists via test_user fixture
        "password": "SecurePass123!",
    }, content_type="application/json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_with_correct_credentials_returns_token(client, test_user):
    response = client.post("/api/auth/login/", {
        "username": "testuser",
        "password": "TestPass123!",
    }, content_type="application/json")

    assert response.status_code == 200
    assert "token" in response.json()


@pytest.mark.django_db
def test_login_with_wrong_password_fails(client, test_user):
    response = client.post("/api/auth/login/", {
        "username": "testuser",
        "password": "WrongPassword!",
    }, content_type="application/json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_resume_upload_requires_authentication(client):
    """Edge case: unauthenticated requests should be rejected."""
    response = client.post("/api/resumes/", {})
    assert response.status_code == 401


@pytest.mark.django_db
def test_resume_upload_extracts_text(auth_client, monkeypatch):
    """Mock PDF extraction so this test doesn't depend on a real PDF file."""
    monkeypatch.setattr(
        "resumes.views.extract_text_from_pdf",
        lambda file: "Extracted resume text with Python and Django."
    )

    fake_pdf = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 fake content", content_type="application/pdf")
    response = auth_client.post("/api/resumes/", {"file": fake_pdf}, format="multipart")

    assert response.status_code == 201
    assert response.json()["extracted_text"] == "Extracted resume text with Python and Django."


@pytest.mark.django_db
def test_analysis_full_flow(auth_client, mock_groq_feedback):
    """End-to-end: create resume + JD, trigger analysis, verify scoring and mocked AI feedback."""
    resume_response = auth_client.post(
        "/api/resumes/",
        {"file": SimpleUploadedFile("resume.pdf", b"%PDF-1.4", content_type="application/pdf")},
        format="multipart",
    )
    resume_id = resume_response.json()["id"]

    # Manually set extracted_text since we're not mocking PDF extraction here
    from resumes.models import Resume
    Resume.objects.filter(id=resume_id).update(extracted_text="I know Python and Django.")

    jd_response = auth_client.post("/api/job-descriptions/", {
        "title": "Backend Role",
        "raw_text": "Need Python, Django, and AWS experience.",
    })
    jd_id = jd_response.json()["id"]

    response = auth_client.post("/api/analyses/", {
        "resume_id": resume_id,
        "job_description_id": jd_id,
    })

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "completed"
    assert data["match_score"] == 67 
    assert "AWS" in data["missing_keywords"]
    assert data["ai_feedback"] == "1. Add more keywords. 2. Improve formatting."

    # Confirm the real Groq function was never actually called
    mock_groq_feedback.assert_called_once()


@pytest.mark.django_db
def test_user_cannot_see_another_users_resume(auth_client, test_user):
    """Security test: confirms the get_queryset filtering actually works."""
    from django.contrib.auth.models import User
    from resumes.models import Resume

    other_user = User.objects.create_user(username="otheruser", password="pass123")
    other_resume = Resume.objects.create(user=other_user, extracted_text="secret resume")

    response = auth_client.get(f"/api/resumes/{other_resume.id}/")
    assert response.status_code == 404
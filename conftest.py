import pytest
from unittest.mock import patch
from rest_framework.authtoken.models import Token


@pytest.fixture
def test_user(db):
    from django.contrib.auth.models import User
    return User.objects.create_user(username="testuser", password="TestPass123!")


@pytest.fixture
def auth_client(test_user):
    from rest_framework.test import APIClient
    token, _ = Token.objects.get_or_create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.fixture
def mock_groq_feedback():
    """Prevents tests from ever calling the real Groq API."""
    with patch("resumes.views.get_ai_feedback") as mock:
        mock.return_value = "1. Add more keywords. 2. Improve formatting."
        yield mock
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from answer_ai.main import app
from answer_ai.routers import auths

# Mock the database dependencies
@pytest.fixture
def mock_users():
    with patch("answer_ai.routers.auths.Users") as mock:
        yield mock

@pytest.fixture
def mock_auths():
    with patch("answer_ai.routers.auths.Auths") as mock:
        yield mock

@pytest.fixture
def client():
    # We need to mock lifespan or ensure it doesn't fail
    with patch("answer_ai.main.get_redis_connection", return_value=None):
        with patch("answer_ai.main.get_all_models"):
            # Mock install_tool_and_function_dependencies
            with patch("answer_ai.main.install_tool_and_function_dependencies"):
                 with TestClient(app) as c:
                    yield c

def test_signup_spam(client, mock_users, mock_auths):
    # Setup mocks
    # Simulate that users already exist so we don't trigger "first user is admin" and "disable signup" logic
    mock_users.has_users.return_value = True
    mock_users.get_user_by_email.return_value = None

    # Mock insert_new_auth to return a user object
    mock_user = MagicMock()
    mock_user.id = "user_id"
    mock_user.email = "test@example.com"
    mock_user.name = "Test User"
    mock_user.role = "user"
    mock_user.profile_image_url = "/image.png"
    # insert_new_auth returns a user object
    mock_auths.insert_new_auth.return_value = mock_user
    mock_auths.authenticate_user_by_email.return_value = mock_user

    # Ensure signup is enabled
    app.state.config.ENABLE_SIGNUP = True

    # Clear rate limiter memory if it exists (for the signup limiter we are about to add)
    if hasattr(auths, "signup_rate_limiter"):
         auths.signup_rate_limiter._memory_store.clear()

    # Attempt 10 signups
    for i in range(10):
        email = f"spammer{i}@example.com"

        response = client.post(
            "/api/v1/auths/signup",
            json={
                "name": f"Spammer {i}",
                "email": email,
                "password": "password123",
            },
        )

        if i < 5:
            assert response.status_code == 200, f"Request {i} failed with {response.status_code}: {response.text}"
        else:
            assert response.status_code == 429, f"Request {i} failed with {response.status_code}: {response.text}"

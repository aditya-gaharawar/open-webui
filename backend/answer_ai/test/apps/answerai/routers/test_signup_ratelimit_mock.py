import pytest
from unittest.mock import MagicMock, patch
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from answer_ai.routers import auths

# Create a minimal app with just the auth router
app = FastAPI()
app.include_router(auths.router, prefix="/api/v1/auths")

# Mock app state
app.state.config = MagicMock()
app.state.config.ENABLE_SIGNUP = True
app.state.config.ENABLE_LOGIN_FORM = True
app.state.config.JWT_EXPIRES_IN = "1h"
app.state.config.DEFAULT_GROUP_ID = "1"
app.state.config.USER_PERMISSIONS = {}
app.state.config.WEBHOOK_URL = ""
app.state.ANSWERAI_NAME = "AnswerAI"

client = TestClient(app)

def test_signup_rate_limit():
    # Force the rate limiter to use memory store and clear it
    auths.signup_rate_limiter.r = None
    auths.signup_rate_limiter._memory_store = {}
    auths.signup_rate_limiter.enabled = True

    # Mock dependencies
    with patch("answer_ai.routers.auths.Users") as mock_users, \
         patch("answer_ai.routers.auths.Auths") as mock_auths, \
         patch("answer_ai.routers.auths.validate_email_format", return_value=True), \
         patch("answer_ai.routers.auths.validate_password"), \
         patch("answer_ai.routers.auths.get_password_hash", return_value="hashed"), \
         patch("answer_ai.routers.auths.create_token", return_value="token"), \
         patch("answer_ai.routers.auths.get_permissions", return_value={}), \
         patch("answer_ai.routers.auths.apply_default_group_assignment"), \
         patch("answer_ai.routers.auths.post_webhook"):

        # Setup mocks - simulate existing users so we don't trigger "first user" logic which disables signup
        mock_users.has_users.return_value = True
        mock_users.get_user_by_email.return_value = None

        mock_user = MagicMock()
        mock_user.id = "123"
        mock_user.email = "test@example.com"
        mock_user.name = "Test"
        mock_user.role = "user"
        mock_user.profile_image_url = ""
        mock_user.model_dump_json.return_value = "{}"

        mock_auths.insert_new_auth.return_value = mock_user
        mock_auths.authenticate_user_by_email.return_value = mock_user

        # Make 5 requests (allowed)
        for i in range(5):
            response = client.post(
                "/api/v1/auths/signup",
                json={
                    "name": "Test",
                    "email": f"test{i}@example.com",
                    "password": "password"
                }
            )
            assert response.status_code == 200, f"Request {i+1} failed: {response.text}"

        # Make 6th request (should be blocked)
        response = client.post(
            "/api/v1/auths/signup",
            json={
                "name": "Test",
                "email": "test6@example.com",
                "password": "password"
            }
        )
        assert response.status_code == 429
        assert "API rate limit exceeded" in response.text

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from answer_ai.utils.rate_limit import RateLimiter
from answer_ai.constants import ERROR_MESSAGES

from answer_ai.main import app
import answer_ai.routers.auths as auths_router

class TestRateLimit:
    def setup_method(self):
        # Reset memory store before each test
        RateLimiter._memory_store = {}

    def teardown_method(self):
        # Reset memory store after each test
        RateLimiter._memory_store = {}

    def test_signup_rate_limit(self):
        client = TestClient(app)

        # Setup mocks using patch.object
        with patch.object(auths_router, 'Users') as mock_users, \
             patch.object(auths_router, 'Auths') as mock_auths, \
             patch.object(auths_router, 'apply_default_group_assignment') as mock_groups, \
             patch.object(auths_router, 'get_permissions') as mock_perms, \
             patch.object(auths_router, 'post_webhook') as mock_webhook:

            mock_users.has_users.return_value = False
            mock_users.get_user_by_email.return_value = None

            mock_user = MagicMock()
            mock_user.id = "1"
            mock_user.email = "test@example.com"
            mock_user.name = "Test"
            mock_user.role = "admin"
            mock_user.profile_image_url = ""
            mock_user.model_dump_json.return_value = "{}"

            mock_auths.insert_new_auth.return_value = mock_user
            mock_perms.return_value = {}

            # Force ENABLE_SIGNUP to True for the request
            app.state.config.ENABLE_SIGNUP = True
            app.state.config.ENABLE_LOGIN_FORM = True

            for i in range(5):
                response = client.post(
                    "/api/v1/auths/signup",
                    json={
                        "name": f"User {i}",
                        "email": f"user{i}@example.com",
                        "password": "password123",
                    },
                )
                assert response.status_code != 429

            # 6th request
            response = client.post(
                "/api/v1/auths/signup",
                json={
                    "name": "User 6",
                    "email": "user6@example.com",
                    "password": "password123",
                },
            )
            assert response.status_code == 429
            assert response.json()["detail"] == ERROR_MESSAGES.RATE_LIMIT_EXCEEDED

    def test_signin_ip_rate_limit(self):
         client = TestClient(app)

         with patch.object(auths_router, 'Users') as mock_users, \
              patch.object(auths_router, 'Auths') as mock_auths:

             # Mock authentication failure to keep it simple
             mock_users.get_user_by_email.return_value = MagicMock()
             mock_auths.authenticate_user.return_value = None # Fail auth

             with patch("answer_ai.routers.auths.ENABLE_PASSWORD_AUTH", True):
                 for i in range(15):
                     response = client.post(
                        "/api/v1/auths/signin",
                        json={"email": f"user{i}@example.com", "password": "password"},
                    )
                     assert response.status_code != 429

                 # 16th
                 response = client.post(
                    "/api/v1/auths/signin",
                    json={"email": "final@example.com", "password": "password"},
                )
                 assert response.status_code == 429
                 assert response.json()["detail"] == ERROR_MESSAGES.RATE_LIMIT_EXCEEDED

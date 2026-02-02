
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI
from answer_ai.utils.rate_limit import RateLimiter
from answer_ai.routers.auths import router
from answer_ai.config import ENABLE_SIGNUP

# Mock the entire config
with patch('answer_ai.config.ENABLE_SIGNUP', True):
    pass

def test_signup_rate_limit():
    # Setup
    app = FastAPI()
    app.include_router(router)
    app.state.config = MagicMock()
    app.state.config.ENABLE_SIGNUP = True
    app.state.config.ENABLE_LOGIN_FORM = True
    app.state.config.JWT_EXPIRES_IN = "1h"
    app.state.config.DEFAULT_USER_ROLE = "user"
    app.state.config.DEFAULT_GROUP_ID = "1"
    app.state.config.USER_PERMISSIONS = {}
    app.state.config.WEBHOOK_URL = ""
    app.state.ANSWERAI_NAME = "Test"

    client = TestClient(app)

    # Clear rate limiter memory store
    RateLimiter._memory_store.clear()

    # Mock DB interactions
    with patch('answer_ai.models.users.Users.get_user_by_email') as mock_get_user, \
         patch('answer_ai.models.auths.Auths.insert_new_auth') as mock_insert, \
         patch('answer_ai.models.users.Users.has_users') as mock_has_users, \
         patch('answer_ai.routers.auths.create_token') as mock_token, \
         patch('answer_ai.routers.auths.apply_default_group_assignment'):

        mock_get_user.return_value = None
        mock_has_users.return_value = True # Assuming users exist

        # Mock insert to return a user object
        mock_user = MagicMock()
        mock_user.id = "1"
        mock_user.email = "test@example.com"
        mock_user.name = "Test"
        mock_user.role = "user"
        mock_user.profile_image_url = ""
        mock_insert.return_value = mock_user

        mock_token.return_value = "token"

        # Mock RateLimiter inside the router module if it's already imported
        # But we are testing that the router *uses* it.
        # Since we haven't modified the router yet, this test should SUCCEED for 6 requests (no rate limit)
        # or fail if we assert 429.

        # We want to reproduce the FAILURE (lack of rate limit).

        for i in range(10):
            response = client.post(
                "/signup",
                json={
                    "name": f"User {i}",
                    "email": f"user{i}@example.com",
                    "password": "password123",
                },
            )
            # Without rate limit, all 10 should succeed (200)
            # If we expect rate limit of 5, the 6th should be 429.

            if i < 5:
                assert response.status_code == 200, f"Request {i} failed: {response.text}"
            else:
                # This assertion expects 429, but currently it will be 200.
                # So this test will FAIL, which is what we want for reproduction.
                assert response.status_code == 429, f"Request {i} should be rate limited but got {response.status_code}"

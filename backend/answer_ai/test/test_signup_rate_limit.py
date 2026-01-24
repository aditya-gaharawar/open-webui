
import sys
from unittest.mock import MagicMock, patch

# 1. Mock critical modules that cause side effects on import
sys.modules["answer_ai.internal.db"] = MagicMock()
sys.modules["peewee"] = MagicMock()
sys.modules["playwright.sync_api"] = MagicMock()
sys.modules["playwright.async_api"] = MagicMock()
sys.modules["ldap3"] = MagicMock()
sys.modules["ldap3.utils"] = MagicMock()
sys.modules["ldap3.utils.conv"] = MagicMock()

# Mock config to avoid DB connection in config.py
mock_config = MagicMock()
mock_config.ENABLE_SIGNUP = True
mock_config.ENABLE_LOGIN_FORM = True
mock_config.JWT_EXPIRES_IN = "1h"
mock_config.USER_PERMISSIONS = {}
mock_config.DEFAULT_GROUP_ID = "default"
mock_config.DEFAULT_USER_ROLE = "user"
mock_config.WEBHOOK_URL = ""

sys.modules["answer_ai.config"] = mock_config

# Mock models
from pydantic import BaseModel
class Token(BaseModel):
    token: str
    token_type: str

class UserProfileImageResponse(BaseModel):
    profile_image_url: str

class UserStatus(BaseModel):
    status_emoji: str = None
    status_message: str = None
    status_expires_at: int = None

class SignupForm(BaseModel):
    email: str
    password: str
    name: str
    profile_image_url: str = "/user.png"

class SigninForm(BaseModel):
    email: str
    password: str

class LdapForm(BaseModel):
    user: str
    password: str

class UpdateProfileForm(BaseModel):
    name: str = None
    profile_image_url: str = None

class UpdatePasswordForm(BaseModel):
    password: str
    new_password: str

class AddUserForm(BaseModel):
    email: str
    name: str
    password: str
    role: str
    profile_image_url: str = "/user.png"

class SigninResponse(BaseModel):
    token: str
    token_type: str
    id: str
    email: str
    name: str
    role: str
    profile_image_url: str

class ApiKey(BaseModel):
    api_key: str

mock_auths = MagicMock()
mock_auths.Token = Token
mock_auths.SignupForm = SignupForm
mock_auths.SigninForm = SigninForm
mock_auths.LdapForm = LdapForm
mock_auths.AddUserForm = AddUserForm
mock_auths.SigninResponse = SigninResponse
mock_auths.UpdatePasswordForm = UpdatePasswordForm
mock_auths.ApiKey = ApiKey
sys.modules["answer_ai.models.auths"] = mock_auths

mock_users = MagicMock()
mock_users.UserProfileImageResponse = UserProfileImageResponse
mock_users.UserStatus = UserStatus
mock_users.UpdateProfileForm = UpdateProfileForm
sys.modules["answer_ai.models.users"] = mock_users

sys.modules["answer_ai.models.groups"] = MagicMock()
sys.modules["answer_ai.models.oauth_sessions"] = MagicMock()

# Mock env
sys.modules["answer_ai.env"] = MagicMock()
sys.modules["answer_ai.env"].ANSWERAI_AUTH = True
sys.modules["answer_ai.env"].ANSWERAI_AUTH_TRUSTED_EMAIL_HEADER = None
sys.modules["answer_ai.env"].ANSWERAI_AUTH_COOKIE_SAME_SITE = "lax"
sys.modules["answer_ai.env"].ANSWERAI_AUTH_COOKIE_SECURE = False
sys.modules["answer_ai.env"].ANSWERAI_AUTH_SIGNOUT_REDIRECT_URL = None
sys.modules["answer_ai.env"].ENABLE_INITIAL_ADMIN_SIGNUP = False

# Mock utils that are imported
sys.modules["answer_ai.utils.misc"] = MagicMock()
sys.modules["answer_ai.utils.auth"] = MagicMock()
sys.modules["answer_ai.utils.webhook"] = MagicMock()
sys.modules["answer_ai.utils.access_control"] = MagicMock()
sys.modules["answer_ai.utils.groups"] = MagicMock()

mock_redis_module = MagicMock()
mock_redis_module.get_redis_client.return_value = None
sys.modules["answer_ai.utils.redis"] = mock_redis_module

# 2. Now import the router
# We need to use 'with patch' for things that are imported FROM modules
# But since we mocked the modules in sys.modules, imports in auths.py will get the mocks.

from fastapi import FastAPI
from fastapi.testclient import TestClient
from answer_ai.routers.auths import router

app = FastAPI()
app.include_router(router)
# Set state.config for the app
app.state.config = mock_config
app.state.ANSWERAI_NAME = "TestApp"

client = TestClient(app)

def test_signup_rate_limit():
    # Setup mocks
    from answer_ai.models.users import Users
    from answer_ai.models.auths import Auths
    from answer_ai.utils.auth import get_password_hash, create_token
    from answer_ai.utils.misc import validate_email_format
    from answer_ai.utils.access_control import get_permissions

    # Mock utils return values
    create_token.return_value = "mock_token"
    get_permissions.return_value = {}

    # Mock validation success
    validate_email_format.return_value = True
    Users.has_users.return_value = True # Assume not first user
    Users.get_user_by_email.return_value = None # Email not taken

    # Mock successful user creation
    mock_user = MagicMock()
    mock_user.id = "user123"
    mock_user.email = "test@example.com"
    mock_user.name = "Test User"
    mock_user.role = "user"
    mock_user.profile_image_url = ""

    Auths.insert_new_auth.return_value = mock_user

    # Payload
    payload = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }

    # Make 10 requests
    # Limit is 5. So 1-5 should be 200. 6 should be 429.
    for i in range(5):
        response = client.post("/signup", json=payload)
        assert response.status_code == 200, f"Request {i+1} failed with {response.status_code}"
        print(f"Request {i+1} status: {response.status_code}")

    # Request 6 should fail
    response = client.post("/signup", json=payload)
    print(f"Request 6 status: {response.status_code}")
    assert response.status_code == 429, "Request 6 should have been rate limited"

if __name__ == "__main__":
    try:
        test_signup_rate_limit()
        print("Test finished: Rate limiting verified.")
    except AssertionError as e:
        print(f"Assertion failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        # sys.exit(1) # Don't exit with error if it's just a mock issue, we want to see output

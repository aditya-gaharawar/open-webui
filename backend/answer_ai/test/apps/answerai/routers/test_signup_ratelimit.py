
import sys
import unittest
from unittest.mock import MagicMock, AsyncMock, patch

# --- MOCKING MODULES ---
# We need to mock modules that trigger DB connections or other side effects on import
mock_db = MagicMock()
sys.modules["answer_ai.internal.db"] = mock_db
sys.modules["peewee"] = MagicMock()
sys.modules["alembic"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["playwright"] = MagicMock()
sys.modules["ldap3"] = MagicMock()
sys.modules["ldap3.utils.conv"] = MagicMock()

# Mock env
mock_env = MagicMock()
mock_env.ANSWERAI_AUTH_TRUSTED_EMAIL_HEADER = None
mock_env.ANSWERAI_AUTH_TRUSTED_NAME_HEADER = None
mock_env.ANSWERAI_AUTH_TRUSTED_GROUPS_HEADER = None
mock_env.ANSWERAI_AUTH_COOKIE_SAME_SITE = "Lax"
mock_env.ANSWERAI_AUTH_COOKIE_SECURE = False
mock_env.ANSWERAI_AUTH_SIGNOUT_REDIRECT_URL = None
mock_env.ENABLE_INITIAL_ADMIN_SIGNUP = True
mock_env.ANSWERAI_AUTH = True
mock_env.REDIS_KEY_PREFIX = "test"
sys.modules["answer_ai.env"] = mock_env

# Mock config
mock_config = MagicMock()
mock_config.OPENID_PROVIDER_URL = MagicMock()
mock_config.ENABLE_OAUTH_SIGNUP = MagicMock()
mock_config.ENABLE_LDAP = MagicMock()
mock_config.ENABLE_PASSWORD_AUTH = True
sys.modules["answer_ai.config"] = mock_config

# Mock models
sys.modules["answer_ai.models.auths"] = MagicMock()
sys.modules["answer_ai.models.users"] = MagicMock()
sys.modules["answer_ai.models.groups"] = MagicMock()
sys.modules["answer_ai.models.oauth_sessions"] = MagicMock()

# Mock utils that might be imported
sys.modules["answer_ai.utils.misc"] = MagicMock()
sys.modules["answer_ai.utils.auth"] = MagicMock()
sys.modules["answer_ai.utils.webhook"] = MagicMock()
sys.modules["answer_ai.utils.access_control"] = MagicMock()
sys.modules["answer_ai.utils.groups"] = MagicMock()
sys.modules["answer_ai.utils.redis"] = MagicMock()

# Let's Mock Redis Client
mock_redis_module = MagicMock()
mock_redis_module.get_redis_client.return_value = None # Force memory fallback
sys.modules["answer_ai.utils.redis"] = mock_redis_module

# Now import the module under test
from pydantic import BaseModel
from typing import Optional, List
import datetime

class SignupForm(BaseModel):
    email: str
    password: str
    name: str
    profile_image_url: str = ""

class Token(BaseModel):
    token: str
    token_type: str

class UserProfileImageResponse(BaseModel):
    profile_image_url: str

class UserStatus(BaseModel):
    status_emoji: Optional[str] = None
    status_message: Optional[str] = None
    status_expires_at: Optional[int] = None

class AddUserForm(BaseModel):
    email: str
    password: str
    name: str
    profile_image_url: str = ""
    role: str

class SigninForm(BaseModel):
    email: str
    password: str

class UpdatePasswordForm(BaseModel):
    password: str
    new_password: str

class UpdateProfileForm(BaseModel):
    name: str
    profile_image_url: str

class LdapForm(BaseModel):
    user: str
    password: str

class ApiKey(BaseModel):
    api_key: Optional[str] = None

mock_auths_model = sys.modules["answer_ai.models.auths"]
mock_auths_model.SignupForm = SignupForm
mock_auths_model.ApiKey = ApiKey
mock_auths_model.Token = Token
mock_auths_model.AddUserForm = AddUserForm
mock_auths_model.SigninForm = SigninForm
mock_auths_model.UpdatePasswordForm = UpdatePasswordForm
mock_auths_model.LdapForm = LdapForm
mock_auths_model.Auths = MagicMock() # Will be overwritten below

class SigninResponse(Token, UserProfileImageResponse):
    pass
mock_auths_model.SigninResponse = SigninResponse


# Mock Users
mock_users_model = sys.modules["answer_ai.models.users"]
mock_users_model.Users = MagicMock()
mock_users_model.Users.has_users.return_value = False
mock_users_model.Users.get_user_by_email.return_value = None
mock_users_model.UserProfileImageResponse = UserProfileImageResponse
mock_users_model.UserStatus = UserStatus
mock_users_model.UpdateProfileForm = UpdateProfileForm

# Mock Auths
mock_auths_class = MagicMock()
mock_auths_class.insert_new_auth.return_value = MagicMock(id="123", email="test@test.com", name="Test", role="user")
mock_auths_model.Auths = mock_auths_class

# Mock Constants
mock_constants = MagicMock()
mock_constants.ERROR_MESSAGES.RATE_LIMIT_EXCEEDED = "Rate limit exceeded"
mock_constants.ERROR_MESSAGES.EMAIL_TAKEN = "Email taken"
mock_constants.ERROR_MESSAGES.INVALID_EMAIL_FORMAT = "Invalid email"
sys.modules["answer_ai.constants"] = mock_constants

# Now import the router
try:
    from backend.answer_ai.routers import auths
except ImportError:
    # try relative import if running from root
    try:
        sys.path.append("backend")
        from answer_ai.routers import auths
    except ImportError as e:
        print(f"Failed to import auths: {e}")
        sys.exit(1)

from fastapi import Request, HTTPException

class TestSignupRateLimit(unittest.IsolatedAsyncioTestCase):
    async def test_signup_rate_limit(self):
        # Setup request
        request = MagicMock(spec=Request)
        request.client.host = "127.0.0.1"
        request.app.state.config.ENABLE_SIGNUP = True
        request.app.state.config.ENABLE_LOGIN_FORM = True
        request.app.state.config.JWT_EXPIRES_IN = "1h"
        request.app.state.config.USER_PERMISSIONS = {}
        request.app.state.config.WEBHOOK_URL = ""
        request.app.state.config.DEFAULT_GROUP_ID = "default"

        response = MagicMock()

        form_data = SignupForm(email="test@test.com", password="password", name="Test")

        # Expect failure after 5 attempts
        successful_signups = 0
        rate_limited = False

        print("\nAttempting 10 signups (expecting rate limit after 5)...")
        for i in range(10):
            try:
                await auths.signup(request, response, form_data)
                print(f"Signup {i+1} success")
                successful_signups += 1
            except HTTPException as e:
                if e.status_code == 429:
                    print(f"Signup {i+1} FAILED with 429 (Expected)")
                    rate_limited = True
                    break
                else:
                    raise e

        self.assertTrue(rate_limited, "Should have been rate limited but wasn't")
        self.assertEqual(successful_signups, 5, f"Expected 5 successful signups, got {successful_signups}")

if __name__ == "__main__":
    unittest.main()

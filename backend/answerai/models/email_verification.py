import logging
import secrets
import time
import uuid
from typing import Optional

from answerai.internal.db import Base, get_db
from answerai.env import SRC_LOG_LEVELS
from pydantic import BaseModel
from sqlalchemy import BigInteger, Column, String, Text, Boolean, ForeignKey

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# DB MODEL
####################


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_token"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    expires_at = Column(BigInteger, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(BigInteger, nullable=False)


class EmailVerificationTokenModel(BaseModel):
    id: str
    user_id: str
    token: str
    email: str
    expires_at: int
    used: bool = False
    created_at: int


####################
# Forms
####################


class VerifyEmailForm(BaseModel):
    token: str


class ResendVerificationEmailForm(BaseModel):
    email: str


####################
# Table Operations
####################


class EmailVerificationTokensTable:
    def create_token(
        self,
        user_id: str,
        email: str,
        expiration_seconds: int = 86400,  # 24 hours default
    ) -> Optional[EmailVerificationTokenModel]:
        """Create a new email verification token"""
        try:
            with get_db() as db:
                token_id = str(uuid.uuid4())
                # Generate a secure random token
                token = secrets.token_urlsafe(32)
                current_time = int(time.time())
                expires_at = current_time + expiration_seconds

                token_model = EmailVerificationTokenModel(
                    id=token_id,
                    user_id=user_id,
                    token=token,
                    email=email,
                    expires_at=expires_at,
                    used=False,
                    created_at=current_time,
                )

                result = EmailVerificationToken(**token_model.model_dump())
                db.add(result)
                db.commit()
                db.refresh(result)

                if result:
                    return token_model
                else:
                    return None
        except Exception as e:
            log.error(f"Error creating verification token: {e}")
            return None

    def get_token_by_token_string(
        self, token: str
    ) -> Optional[EmailVerificationTokenModel]:
        """Get a verification token by its token string"""
        try:
            with get_db() as db:
                token_obj = (
                    db.query(EmailVerificationToken).filter_by(token=token).first()
                )
                if token_obj:
                    return EmailVerificationTokenModel.model_validate(token_obj)
                return None
        except Exception as e:
            log.error(f"Error getting token: {e}")
            return None

    def verify_token(self, token: str) -> tuple[bool, Optional[str], Optional[str]]:
        """
        Verify a token and return (is_valid, user_id, error_message)
        Note: This only validates the token, does not mark it as used.
        Call mark_token_as_used() after successfully updating the user.
        """
        try:
            with get_db() as db:
                token_obj = (
                    db.query(EmailVerificationToken).filter_by(token=token).first()
                )

                if not token_obj:
                    return False, None, "Invalid verification token"

                if token_obj.used:
                    return False, None, "Verification token already used"

                current_time = int(time.time())
                if current_time > token_obj.expires_at:
                    return False, None, "Verification token has expired"

                return True, token_obj.user_id, None
        except Exception as e:
            log.error(f"Error verifying token: {e}")
            return False, None, "An error occurred during verification"

    def mark_token_as_used(self, token: str) -> bool:
        """
        Mark a token as used. Call this AFTER successfully updating the user.
        """
        try:
            with get_db() as db:
                db.query(EmailVerificationToken).filter_by(token=token).update(
                    {"used": True}
                )
                db.commit()
                return True
        except Exception as e:
            log.error(f"Error marking token as used: {e}")
            return False

    def delete_expired_tokens(self) -> int:
        """Delete all expired tokens"""
        try:
            with get_db() as db:
                current_time = int(time.time())
                result = (
                    db.query(EmailVerificationToken)
                    .filter(EmailVerificationToken.expires_at < current_time)
                    .delete()
                )
                db.commit()
                return result
        except Exception as e:
            log.error(f"Error deleting expired tokens: {e}")
            return 0

    def delete_tokens_by_user_id(self, user_id: str) -> bool:
        """Delete all tokens for a specific user"""
        try:
            with get_db() as db:
                db.query(EmailVerificationToken).filter_by(user_id=user_id).delete()
                db.commit()
                return True
        except Exception as e:
            log.error(f"Error deleting user tokens: {e}")
            return False

    def get_unused_token_by_user_id(
        self, user_id: str
    ) -> Optional[EmailVerificationTokenModel]:
        """Get the most recent unused token for a user"""
        try:
            with get_db() as db:
                current_time = int(time.time())
                token_obj = (
                    db.query(EmailVerificationToken)
                    .filter_by(user_id=user_id, used=False)
                    .filter(EmailVerificationToken.expires_at > current_time)
                    .order_by(EmailVerificationToken.created_at.desc())
                    .first()
                )

                if token_obj:
                    return EmailVerificationTokenModel.model_validate(token_obj)
                return None
        except Exception as e:
            log.error(f"Error getting unused token: {e}")
            return None


EmailVerificationTokens = EmailVerificationTokensTable()

import time
import uuid
import hashlib
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Text, Index

from answerai.internal.db import Base, get_db


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_token"

    id = Column(Text, primary_key=True)
    user_id = Column(Text, nullable=False)
    token_hash = Column(String(255), nullable=False, unique=True)
    expires_at = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, nullable=False)

    __table_args__ = (
        Index("idx_email_verification_user_id", "user_id"),
        Index("idx_email_verification_expires_at", "expires_at"),
    )


class EmailVerificationTokenModel(BaseModel):
    id: str
    user_id: str
    token_hash: str
    expires_at: int
    created_at: int

    model_config = ConfigDict(from_attributes=True)


class EmailVerificationsTable:
    DEFAULT_EXPIRY_SECONDS = 60 * 60 * 24  # 24h

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def create_token(
        self, user_id: str, token: str, expires_in_seconds: Optional[int] = None
    ) -> Optional[EmailVerificationTokenModel]:
        now = int(time.time())
        expires_at = now + int(expires_in_seconds or self.DEFAULT_EXPIRY_SECONDS)
        try:
            with get_db() as db:
                # Remove previous tokens for user
                db.query(EmailVerificationToken).filter_by(user_id=user_id).delete()

                token_row = EmailVerificationToken(
                    **{
                        "id": str(uuid.uuid4()),
                        "user_id": user_id,
                        "token_hash": self._hash_token(token),
                        "expires_at": expires_at,
                        "created_at": now,
                    }
                )
                db.add(token_row)
                db.commit()
                db.refresh(token_row)
                return EmailVerificationTokenModel.model_validate(token_row)
        except Exception:
            return None

    def get_by_token(self, token: str) -> Optional[EmailVerificationTokenModel]:
        token_hash = self._hash_token(token)
        try:
            with get_db() as db:
                row = (
                    db.query(EmailVerificationToken)
                    .filter_by(token_hash=token_hash)
                    .first()
                )
                return (
                    EmailVerificationTokenModel.model_validate(row) if row else None
                )
        except Exception:
            return None

    def delete_by_user_id(self, user_id: str) -> bool:
        try:
            with get_db() as db:
                db.query(EmailVerificationToken).filter_by(user_id=user_id).delete()
                db.commit()
                return True
        except Exception:
            return False


EmailVerifications = EmailVerificationsTable()

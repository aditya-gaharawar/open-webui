import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

from answerai.models.email_verification import (
    EmailVerificationTokens,
    VerifyEmailForm,
    ResendVerificationEmailForm,
)
from answerai.models.users import Users
from answerai.utils.email import (
    send_verification_email,
    send_welcome_email,
    is_email_configured,
    EMAIL_VERIFICATION_ENABLED,
    EMAIL_VERIFICATION_URL,
    EMAIL_VERIFICATION_TOKEN_EXPIRY,
)
from answerai.utils.auth import get_current_user
from answerai.constants import ERROR_MESSAGES
from answerai.env import SRC_LOG_LEVELS

router = APIRouter()

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MAIN"])

####################
# Response Models
####################


class EmailVerificationStatusResponse(BaseModel):
    enabled: bool
    email_verified: bool


class VerifyEmailResponse(BaseModel):
    success: bool
    message: str
    email_verified: bool


class ResendVerificationResponse(BaseModel):
    success: bool
    message: str


####################
# Email Verification Status
####################


@router.get("/status", response_model=EmailVerificationStatusResponse)
async def get_email_verification_status(user=Depends(get_current_user)):
    """Get email verification status for the current user"""
    user_data = Users.get_user_by_id(user.id)
    
    email_verified = True  # Default to True if verification is disabled
    if EMAIL_VERIFICATION_ENABLED and user_data:
        # Check if user has email_verified attribute
        email_verified = getattr(user_data, "email_verified", True)
    
    return {
        "enabled": EMAIL_VERIFICATION_ENABLED and is_email_configured(),
        "email_verified": email_verified,
    }


####################
# Verify Email
####################


@router.post("/verify", response_model=VerifyEmailResponse)
async def verify_email(form_data: VerifyEmailForm):
    """Verify email address using the token from the verification link"""
    
    if not EMAIL_VERIFICATION_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email verification is not enabled",
        )

    if not is_email_configured():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email is not properly configured",
        )

    # Verify the token
    is_valid, user_id, error_message = EmailVerificationTokens.verify_token(
        form_data.token
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message or "Invalid verification token",
        )

    # Update user's email_verified status
    user = Users.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Update the user's email verification status
    updated_user = Users.update_user_by_id(user_id, {"email_verified": True})

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user verification status",
        )

    # Send welcome email (optional, don't fail if it doesn't send)
    try:
        send_welcome_email(user.email, user.name)
    except Exception as e:
        log.warning(f"Failed to send welcome email: {e}")

    log.info(f"Email verified successfully for user {user_id}")

    return {
        "success": True,
        "message": "Email verified successfully",
        "email_verified": True,
    }


####################
# Resend Verification Email
####################


@router.post("/resend", response_model=ResendVerificationResponse)
async def resend_verification_email(form_data: ResendVerificationEmailForm):
    """Resend verification email to the user"""
    
    if not EMAIL_VERIFICATION_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email verification is not enabled",
        )

    if not is_email_configured():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email is not properly configured",
        )

    # Get user by email
    user = Users.get_user_by_email(form_data.email.lower())
    if not user:
        # Don't reveal if the email exists or not for security reasons
        return {
            "success": True,
            "message": "If the email exists, a verification link has been sent",
        }

    # Check if user is already verified
    email_verified = getattr(user, "email_verified", False)
    if email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified",
        )

    # Check if there's an existing unused token
    existing_token = EmailVerificationTokens.get_unused_token_by_user_id(user.id)
    if existing_token:
        # Reuse existing token if it's still valid
        token_string = existing_token.token
    else:
        # Create new verification token
        token = EmailVerificationTokens.create_token(
            user_id=user.id,
            email=user.email,
            expiration_seconds=EMAIL_VERIFICATION_TOKEN_EXPIRY,
        )

        if not token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create verification token",
            )
        
        token_string = token.token

    # Send verification email
    success, error = send_verification_email(
        to_email=user.email,
        user_name=user.name,
        verification_token=token_string,
        base_url=EMAIL_VERIFICATION_URL,
    )

    if not success:
        log.error(f"Failed to send verification email: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email",
        )

    log.info(f"Verification email sent to {user.email}")

    return {
        "success": True,
        "message": "Verification email has been sent",
    }


####################
# Check if Email Verification is Required
####################


@router.get("/required")
async def is_email_verification_required():
    """Check if email verification is required for the system"""
    return {
        "required": EMAIL_VERIFICATION_ENABLED and is_email_configured(),
        "configured": is_email_configured(),
    }

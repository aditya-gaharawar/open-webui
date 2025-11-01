"""add email verification

Revision ID: e47b8c9d3f21
Revises: d31026856c01
Create Date: 2025-10-21 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e47b8c9d3f21"
down_revision = "d31026856c01"
branch_labels = None
depends_on = None


def upgrade():
    # Add email_verified column to user table with nullable=True initially
    op.add_column(
        "user",
        sa.Column("email_verified", sa.Boolean(), nullable=True),
    )

    # Set all existing users to email_verified=True (they were already using the system)
    # This prevents locking out existing users when email verification is enabled
    op.execute("UPDATE user SET email_verified = true WHERE email_verified IS NULL")

    # Now set the default for future rows
    op.alter_column(
        "user",
        "email_verified",
        server_default=sa.text("false"),
        nullable=True,
    )

    # Create email_verification_token table
    op.create_table(
        "email_verification_token",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("expires_at", sa.BigInteger(), nullable=False),
        sa.Column("used", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("token"),
    )

    # Create indexes for better query performance
    op.create_index(
        op.f("ix_email_verification_token_user_id"),
        "email_verification_token",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_email_verification_token_email"),
        "email_verification_token",
        ["email"],
        unique=False,
    )
    op.create_index(
        op.f("ix_email_verification_token_expires_at"),
        "email_verification_token",
        ["expires_at"],
        unique=False,
    )


def downgrade():
    # Drop indexes
    op.drop_index(
        op.f("ix_email_verification_token_expires_at"),
        table_name="email_verification_token",
    )
    op.drop_index(
        op.f("ix_email_verification_token_email"), table_name="email_verification_token"
    )
    op.drop_index(
        op.f("ix_email_verification_token_user_id"),
        table_name="email_verification_token",
    )

    # Drop email_verification_token table
    op.drop_table("email_verification_token")

    # Remove email_verified column from user table
    op.drop_column("user", "email_verified")

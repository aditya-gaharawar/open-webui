"""Peewee migrations -- 019_add_email_verification.py.
"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""

    # Add email_verified_at to user table
    migrator.add_fields(
        "user",
        email_verified_at=pw.BigIntegerField(null=True),
    )

    # Create email_verification_token table
    @migrator.create_model
    class EmailVerificationToken(pw.Model):
        id = pw.CharField(max_length=255, unique=True)
        user_id = pw.CharField(max_length=255)
        token_hash = pw.CharField(max_length=255, unique=True)
        expires_at = pw.BigIntegerField()
        created_at = pw.BigIntegerField()

        class Meta:
            table_name = "email_verification_token"


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""

    migrator.remove_fields("user", "email_verified_at")
    migrator.remove_model("email_verification_token")

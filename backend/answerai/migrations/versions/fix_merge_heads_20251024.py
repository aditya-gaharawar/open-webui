"""Merge heads a5c220713937 and e47b8c9d3f21

Revision ID: f_merge_20251024
Revises: a5c220713937, e47b8c9d3f21
Create Date: 2025-10-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f_merge_20251024"
down_revision: Union[str, tuple[str, ...]] = ("a5c220713937", "e47b8c9d3f21")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Merge revision - no schema changes
    pass


def downgrade() -> None:
    # No-op; cannot un-merge branches
    pass

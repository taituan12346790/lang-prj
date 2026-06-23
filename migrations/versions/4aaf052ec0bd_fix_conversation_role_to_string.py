"""fix_conversation_role_to_string

Revision ID: 4aaf052ec0bd
Revises: 4f6bf87597c2
Create Date: 2026-06-04 14:46:32.019920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4aaf052ec0bd'
down_revision: Union[str, Sequence[str], None] = '4f6bf87597c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - change role column from enum to string"""
    # Drop the old enum constraint and change to varchar
    op.alter_column(
        'conversations',
        'role',
        existing_type=sa.String(length=20),
        type_=sa.String(20),
        existing_nullable=False
    )


def downgrade() -> None:
    """Downgrade schema"""
    pass


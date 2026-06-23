"""add_onboarding_completed_to_user_profile

Revision ID: f6c7b58afddd
Revises: 4f6bf87597c3
Create Date: 2026-06-09 19:17:48.176020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6c7b58afddd'
down_revision: Union[str, Sequence[str], None] = '4f6bf87597c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add onboarding_completed column with default True for existing users
    op.add_column('user_profiles', 
        sa.Column('onboarding_completed', sa.Boolean(), nullable=False, server_default='true')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user_profiles', 'onboarding_completed')

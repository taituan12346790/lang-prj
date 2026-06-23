"""add study_streak to users

Revision ID: 009_study_streak
Revises: 860e1ee93883
Create Date: 2026-06-24

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '009_study_streak'
down_revision = '860e1ee93883'  # Previous migration
branch_labels = None
depends_on = None


def upgrade():
    # Add study_streak and last_study_date columns to users table
    op.add_column('users', sa.Column('study_streak', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('users', sa.Column('last_study_date', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    # Remove columns if rolling back
    op.drop_column('users', 'last_study_date')
    op.drop_column('users', 'study_streak')

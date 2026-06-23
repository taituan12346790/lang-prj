"""add review columns to user_topic_progress

Revision ID: 010_review_columns
Revises: 009_study_streak
Create Date: 2026-06-24

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = '010_review_columns'
down_revision = '009_study_streak'
branch_labels = None
depends_on = None


def upgrade():
    # Add next_review_date and weak_skills columns to user_topic_progress table
    op.add_column('user_topic_progress', sa.Column('next_review_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('user_topic_progress', sa.Column('weak_skills', JSONB, nullable=True))


def downgrade():
    # Remove columns if rolling back
    op.drop_column('user_topic_progress', 'weak_skills')
    op.drop_column('user_topic_progress', 'next_review_date')

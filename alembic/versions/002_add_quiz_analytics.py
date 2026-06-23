"""add quiz analytics fields

Revision ID: 002_quiz_analytics
Revises: 001
Create Date: 2026-06-04

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '002_quiz_analytics'
down_revision = '001_learning_path'
branch_labels = None
depends_on = None


def upgrade():
    # Add next_review_date to user_topic_progress for spaced repetition
    op.add_column('user_topic_progress', 
        sa.Column('next_review_date', sa.DateTime(timezone=True), nullable=True)
    )
    
    # Add weak_skills tracking to user_topic_progress
    op.add_column('user_topic_progress',
        sa.Column('weak_skills', JSONB, nullable=True)
    )
    
    # Add study_streak to users for gamification
    op.add_column('users',
        sa.Column('study_streak', sa.Integer, default=0, nullable=False, server_default='0')
    )
    
    op.add_column('users',
        sa.Column('last_study_date', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade():
    op.drop_column('users', 'last_study_date')
    op.drop_column('users', 'study_streak')
    op.drop_column('user_topic_progress', 'weak_skills')
    op.drop_column('user_topic_progress', 'next_review_date')

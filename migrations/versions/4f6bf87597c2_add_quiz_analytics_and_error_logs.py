"""add_quiz_analytics_and_error_logs

Revision ID: 4f6bf87597c2
Revises: 001_learning_path
Create Date: 2026-06-04 13:54:56.306583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers, used by Alembic.
revision: str = '4f6bf87597c2'
down_revision: Union[str, Sequence[str], None] = '001_learning_path'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Only create user_error_logs table (analytics fields already exist)
    op.create_table(
        'user_error_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('error_type', sa.String(100), nullable=False, index=True),
        sa.Column('skill_tag', sa.String(100), nullable=False, index=True),
        sa.Column('severity', sa.String(20), default='MEDIUM'),
        sa.Column('user_input', sa.Text(), nullable=False),
        sa.Column('user_answer', sa.Text()),
        sa.Column('correct_form', sa.Text(), nullable=False),
        sa.Column('question', sa.Text()),
        sa.Column('lesson_id', UUID(as_uuid=True), sa.ForeignKey('lessons.id', ondelete='SET NULL')),
        sa.Column('topic_id', UUID(as_uuid=True), sa.ForeignKey('topics.id', ondelete='SET NULL')),
        sa.Column('explanation', sa.Text()),
        sa.Column('suggestion', sa.Text()),
        sa.Column('extra_data', JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Create indexes for better query performance
    op.create_index('idx_error_logs_user_type', 'user_error_logs', ['user_id', 'error_type'])
    op.create_index('idx_error_logs_user_skill', 'user_error_logs', ['user_id', 'skill_tag'])
    op.create_index('idx_error_logs_created', 'user_error_logs', ['created_at'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop error logs table only
    op.drop_index('idx_error_logs_created', 'user_error_logs')
    op.drop_index('idx_error_logs_user_skill', 'user_error_logs')
    op.drop_index('idx_error_logs_user_type', 'user_error_logs')
    op.drop_table('user_error_logs')


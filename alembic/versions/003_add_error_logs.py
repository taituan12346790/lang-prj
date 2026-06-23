"""add error logs table

Revision ID: 003
Revises: 002
Create Date: 2026-06-04 13:30:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002_quiz_analytics'
branch_labels = None
depends_on = None


def upgrade():
    # Create user_error_logs table
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


def downgrade():
    op.drop_index('idx_error_logs_created', 'user_error_logs')
    op.drop_index('idx_error_logs_user_skill', 'user_error_logs')
    op.drop_index('idx_error_logs_user_type', 'user_error_logs')
    op.drop_table('user_error_logs')

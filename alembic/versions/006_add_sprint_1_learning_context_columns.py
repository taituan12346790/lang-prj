"""Add Sprint 1 learning context columns to user_profiles

Revision ID: 4f6bf87597c3
Revises: 4aaf052ec0bd
Create Date: 2026-06-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f6bf87597c3'
down_revision = '4aaf052ec0bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add Sprint 1 learning context columns
    op.add_column('user_profiles', sa.Column('active_topic_id', sa.String(50), nullable=True))
    op.add_column('user_profiles', sa.Column('active_lesson_order', sa.Integer(), nullable=True))
    op.add_column('user_profiles', sa.Column('learning_mode', sa.String(50), nullable=False, server_default='normal'))
    op.add_column('user_profiles', sa.Column('last_chat_session_id', sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column('user_profiles', 'last_chat_session_id')
    op.drop_column('user_profiles', 'learning_mode')
    op.drop_column('user_profiles', 'active_lesson_order')
    op.drop_column('user_profiles', 'active_topic_id')

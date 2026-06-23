"""Add learning context columns to user_profiles

Revision ID: 004
Revises: 003
Create Date: 2026-06-04 21:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns to user_profiles
    op.add_column('user_profiles', sa.Column('active_topic_id', sa.String(length=50), nullable=True))
    op.add_column('user_profiles', sa.Column('active_lesson_order', sa.Integer(), nullable=True))
    op.add_column('user_profiles', sa.Column('learning_mode', sa.String(length=50), nullable=True, server_default='normal'))
    op.add_column('user_profiles', sa.Column('last_chat_session_id', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('user_profiles', 'last_chat_session_id')
    op.drop_column('user_profiles', 'learning_mode')
    op.drop_column('user_profiles', 'active_lesson_order')
    op.drop_column('user_profiles', 'active_topic_id')

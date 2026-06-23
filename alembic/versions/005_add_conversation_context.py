"""Add topic_id and learning_mode to conversations

Revision ID: 005
Revises: 004
Create Date: 2026-06-04 22:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns to conversations
    op.add_column('conversations', sa.Column('topic_id', sa.String(length=50), nullable=True))
    op.add_column('conversations', sa.Column('learning_mode', sa.String(length=50), nullable=True, server_default='normal'))


def downgrade() -> None:
    op.drop_column('conversations', 'learning_mode')
    op.drop_column('conversations', 'topic_id')

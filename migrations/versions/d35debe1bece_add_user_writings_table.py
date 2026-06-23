"""add_user_writings_table

Revision ID: d35debe1bece
Revises: c8e5271d513c
Create Date: 2026-06-10 15:49:22.945315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd35debe1bece'
down_revision: Union[str, Sequence[str], None] = 'c8e5271d513c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user_writings',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('lesson_id', sa.UUID(), nullable=False),
        sa.Column('topic_id', sa.UUID(), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('user_text', sa.Text(), nullable=False),
        sa.Column('word_count', sa.Integer(), nullable=False),
        sa.Column('attempt_number', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('score_grammar', sa.Float(), nullable=True),
        sa.Column('score_vocabulary', sa.Float(), nullable=True),
        sa.Column('score_content', sa.Float(), nullable=True),
        sa.Column('score_structure', sa.Float(), nullable=True),
        sa.Column('score_total', sa.Float(), nullable=True),
        sa.Column('detailed_feedback', sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_user_writings_user_id', 'user_writings', ['user_id'])
    op.create_index('ix_user_writings_lesson_id', 'user_writings', ['lesson_id'])
    op.create_index('ix_user_writings_topic_id', 'user_writings', ['topic_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_user_writings_topic_id', 'user_writings')
    op.drop_index('ix_user_writings_lesson_id', 'user_writings')
    op.drop_index('ix_user_writings_user_id', 'user_writings')
    op.drop_table('user_writings')

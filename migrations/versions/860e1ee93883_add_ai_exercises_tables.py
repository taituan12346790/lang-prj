"""add_ai_exercises_tables

Revision ID: 860e1ee93883
Revises: d35debe1bece
Create Date: 2026-06-10 18:02:10.285866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '860e1ee93883'
down_revision: Union[str, Sequence[str], None] = 'd35debe1bece'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create ai_exercises table
    op.create_table(
        'ai_exercises',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('session_id', sa.UUID(), nullable=True),
        sa.Column('error_type', sa.String(), nullable=False),
        sa.Column('skill_tag', sa.String(), nullable=False),
        sa.Column('frequency', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('original_question', sa.String(), nullable=True),
        sa.Column('user_wrong_answer', sa.String(), nullable=True),
        sa.Column('correct_answer', sa.String(), nullable=True),
        sa.Column('exercises', sa.dialects.postgresql.JSONB(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'IN_PROGRESS', 'COMPLETED', name='exercisestatus'), nullable=False, server_default='PENDING'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['session_id'], ['conversations.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_ai_exercises_user_id', 'ai_exercises', ['user_id'])
    op.create_index('ix_ai_exercises_session_id', 'ai_exercises', ['session_id'])
    
    # Create ai_exercise_submissions table
    op.create_table(
        'ai_exercise_submissions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('exercise_id', sa.UUID(), nullable=False),
        sa.Column('user_answers', sa.dialects.postgresql.JSONB(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('total', sa.Integer(), nullable=False),
        sa.Column('feedback', sa.String(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['exercise_id'], ['ai_exercises.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_ai_exercise_submissions_exercise_id', 'ai_exercise_submissions', ['exercise_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_ai_exercise_submissions_exercise_id', 'ai_exercise_submissions')
    op.drop_table('ai_exercise_submissions')
    
    op.drop_index('ix_ai_exercises_session_id', 'ai_exercises')
    op.drop_index('ix_ai_exercises_user_id', 'ai_exercises')
    op.drop_table('ai_exercises')
    
    op.execute("DROP TYPE exercisestatus")

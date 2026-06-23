"""Add topics, lessons, user_topic_progress tables

Revision ID: 001_learning_path
Revises: 
Create Date: 2026-06-03
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_learning_path'
down_revision = '1d22be5d1e48'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── topics ──────────────────────────────────────────────────
    op.create_table(
        'topics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('level', sa.String(length=2), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('name_vi', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('description_vi', sa.Text(), nullable=True),
        sa.Column('grammar_focus', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('vocabulary_tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('estimated_minutes', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_topics_id', 'topics', ['id'], unique=False)
    op.create_index('ix_topics_level', 'topics', ['level'], unique=False)

    # ── lessons ─────────────────────────────────────────────────
    op.create_table(
        'lessons',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('topic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('lesson_type', sa.String(length=20), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('title_vi', sa.String(length=200), nullable=True),
        sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_lessons_id', 'lessons', ['id'], unique=False)
    op.create_index('ix_lessons_topic_id', 'lessons', ['topic_id'], unique=False)

    # ── user_topic_progress ─────────────────────────────────────
    op.create_table(
        'user_topic_progress',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('topic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='not_started'),
        sa.Column('lesson_completed', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('quiz_score', sa.Float(), nullable=True),
        sa.Column('quiz_attempts', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_activity', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_user_topic_unique', 'user_topic_progress',
                    ['user_id', 'topic_id'], unique=True)


def downgrade() -> None:
    op.drop_table('user_topic_progress')
    op.drop_table('lessons')
    op.drop_table('topics')

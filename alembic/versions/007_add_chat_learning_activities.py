"""add chat learning activities table

Revision ID: 007
Revises: 006
Create Date: 2026-06-09

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade():
    # Create chat_learning_activities table
    op.create_table(
        'chat_learning_activities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chat_session_id', sa.String(), nullable=False),
        sa.Column('activity_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('custom_topic', sa.String(length=100), nullable=True),
        sa.Column('curriculum_topic_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('curriculum_lesson_order', sa.Integer(), nullable=True),
        sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('skill_tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('source', sa.String(length=50), nullable=False, server_default='ai_tutor_chat'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['curriculum_topic_id'], ['topics.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('ix_chat_activity_user_type', 'chat_learning_activities', ['user_id', 'activity_type'])
    op.create_index('ix_chat_activity_user_created', 'chat_learning_activities', ['user_id', 'created_at'])
    op.create_index('ix_chat_activity_session', 'chat_learning_activities', ['chat_session_id', 'created_at'])
    op.create_index(op.f('ix_chat_learning_activities_activity_type'), 'chat_learning_activities', ['activity_type'])
    op.create_index(op.f('ix_chat_learning_activities_chat_session_id'), 'chat_learning_activities', ['chat_session_id'])
    op.create_index(op.f('ix_chat_learning_activities_created_at'), 'chat_learning_activities', ['created_at'])
    op.create_index(op.f('ix_chat_learning_activities_user_id'), 'chat_learning_activities', ['user_id'])


def downgrade():
    # Drop indexes
    op.drop_index(op.f('ix_chat_learning_activities_user_id'), table_name='chat_learning_activities')
    op.drop_index(op.f('ix_chat_learning_activities_created_at'), table_name='chat_learning_activities')
    op.drop_index(op.f('ix_chat_learning_activities_chat_session_id'), table_name='chat_learning_activities')
    op.drop_index(op.f('ix_chat_learning_activities_activity_type'), table_name='chat_learning_activities')
    op.drop_index('ix_chat_activity_session', table_name='chat_learning_activities')
    op.drop_index('ix_chat_activity_user_created', table_name='chat_learning_activities')
    op.drop_index('ix_chat_activity_user_type', table_name='chat_learning_activities')
    
    # Drop table
    op.drop_table('chat_learning_activities')

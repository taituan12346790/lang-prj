"""add is_verified to users table

Revision ID: 1d22be5d1e48
Revises: 
Create Date: 2026-05-27 19:57:08.859099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1d22be5d1e48'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - CREATE base tables."""
    # CREATE base tables from downgrade() logic
    op.create_table('users',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('full_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('google_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('avatar_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('auth_provider', sa.VARCHAR(), server_default=sa.text("'local'::character varying"), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    sa.Column('is_verified', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('last_login', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('google_id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.create_index('ix_users_google_id', 'users', ['google_id'], unique=False)
    
    op.create_table('user_profiles',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('native_language', sa.VARCHAR(), server_default=sa.text("'vi'::character varying"), autoincrement=False, nullable=False),
    sa.Column('target_language', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('current_level', sa.VARCHAR(), server_default=sa.text("'A1'::character varying"), autoincrement=False, nullable=False),
    sa.Column('placement_score', sa.DOUBLE_PRECISION(precision=53), server_default=sa.text('0.0'), autoincrement=False, nullable=True),
    sa.Column('weak_skills', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('strong_skills', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('learning_style', sa.VARCHAR(), server_default=sa.text("'balanced'::character varying"), autoincrement=False, nullable=False),
    sa.Column('interests', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('goals', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('preferred_topics', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('total_sessions', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('total_conversations', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('streak_days', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('last_active', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index('ix_user_profiles_id', 'user_profiles', ['id'], unique=False)
    op.create_index('ix_user_profiles_user_id', 'user_profiles', ['user_id'], unique=False)
    
    op.create_table('memory_entries',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('skill_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('skill_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('frequency', sa.INTEGER(), server_default=sa.text('1'), autoincrement=False, nullable=True),
    sa.Column('confidence_score', sa.DOUBLE_PRECISION(precision=53), server_default=sa.text('0.0'), autoincrement=False, nullable=True),
    sa.Column('last_seen', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'skill_name')
    )
    op.create_index('ix_memory_entries_id', 'memory_entries', ['id'], unique=False)
    op.create_index('ix_memory_entries_skill_name', 'memory_entries', ['skill_name'], unique=False)
    op.create_index('ix_memory_entries_skill_type', 'memory_entries', ['skill_type'], unique=False)
    op.create_index('ix_memory_entries_user_id', 'memory_entries', ['user_id'], unique=False)
    
    op.create_table('conversations',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('session_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('role', postgresql.ENUM('user', 'assistant', name='message_role'), autoincrement=False, nullable=False),
    sa.Column('message', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('tokens', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('model_used', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_session_created', 'conversations', ['session_id', 'created_at'], unique=False)
    op.create_index('ix_conversations_id', 'conversations', ['id'], unique=False)
    op.create_index('ix_conversations_session_id', 'conversations', ['session_id'], unique=False)
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'], unique=False)
    
    op.create_table('learning_sessions',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('session_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('level', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('duration_minutes', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('metrics', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('summary', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_learning_sessions_session_date', 'learning_sessions', ['session_date'], unique=False)
    op.create_index('ix_learning_sessions_user_id', 'learning_sessions', ['user_id'], unique=False)
    
    op.create_table('exercise_results',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('session_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('exercise_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('exercise_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('user_answer', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('expected_answer', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('is_correct', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.Column('skill_tag', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('difficulty', sa.VARCHAR(), server_default=sa.text("'medium'::character varying"), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['learning_sessions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_exercise_results_created_at', 'exercise_results', ['created_at'], unique=False)
    op.create_index('ix_exercise_results_exercise_type', 'exercise_results', ['exercise_type'], unique=False)
    op.create_index('ix_exercise_results_session_id', 'exercise_results', ['session_id'], unique=False)
    op.create_index('ix_exercise_results_skill_tag', 'exercise_results', ['skill_tag'], unique=False)
    op.create_index('ix_exercise_results_user_id', 'exercise_results', ['user_id'], unique=False)
    op.create_index('ix_exercise_session_created', 'exercise_results', ['session_id', 'created_at'], unique=False)
    op.create_index('ix_exercise_user_created', 'exercise_results', ['user_id', 'created_at'], unique=False)
    op.create_index('ix_exercise_user_skill', 'exercise_results', ['user_id', 'skill_tag'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('full_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('google_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('avatar_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('auth_provider', sa.VARCHAR(), server_default=sa.text("'local'::character varying"), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('last_login', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('users_pkey')),
    sa.UniqueConstraint('email', name=op.f('users_email_key'), postgresql_include=[], postgresql_nulls_not_distinct=False),
    sa.UniqueConstraint('google_id', name=op.f('users_google_id_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    op.create_index(op.f('ix_users_google_id'), 'users', ['google_id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_table('memory_entries',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('skill_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('skill_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('frequency', sa.INTEGER(), server_default=sa.text('1'), autoincrement=False, nullable=True),
    sa.Column('confidence_score', sa.DOUBLE_PRECISION(precision=53), server_default=sa.text('0.0'), autoincrement=False, nullable=True),
    sa.Column('last_seen', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('memory_entries_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('memory_entries_pkey')),
    sa.UniqueConstraint('user_id', 'skill_name', name=op.f('memory_entries_user_id_skill_name_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    op.create_index(op.f('ix_memory_entries_user_id'), 'memory_entries', ['user_id'], unique=False)
    op.create_index(op.f('ix_memory_entries_skill_type'), 'memory_entries', ['skill_type'], unique=False)
    op.create_index(op.f('ix_memory_entries_skill_name'), 'memory_entries', ['skill_name'], unique=False)
    op.create_index(op.f('ix_memory_entries_id'), 'memory_entries', ['id'], unique=False)
    op.create_table('user_profiles',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('native_language', sa.VARCHAR(), server_default=sa.text("'vi'::character varying"), autoincrement=False, nullable=False),
    sa.Column('target_language', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('current_level', sa.VARCHAR(), server_default=sa.text("'A1'::character varying"), autoincrement=False, nullable=False),
    sa.Column('placement_score', sa.DOUBLE_PRECISION(precision=53), server_default=sa.text('0.0'), autoincrement=False, nullable=True),
    sa.Column('weak_skills', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('strong_skills', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('learning_style', sa.VARCHAR(), server_default=sa.text("'balanced'::character varying"), autoincrement=False, nullable=False),
    sa.Column('interests', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('goals', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('preferred_topics', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('total_sessions', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('total_conversations', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('streak_days', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('last_active', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('user_profiles_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('user_profiles_pkey')),
    sa.UniqueConstraint('user_id', name=op.f('user_profiles_user_id_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    op.create_index(op.f('ix_user_profiles_user_id'), 'user_profiles', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_profiles_id'), 'user_profiles', ['id'], unique=False)
    op.create_table('conversations',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('session_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('role', postgresql.ENUM('user', 'assistant', name='message_role'), autoincrement=False, nullable=False),
    sa.Column('message', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('tokens', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('model_used', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('conversations_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('conversations_pkey'))
    )
    op.create_index(op.f('ix_conversations_user_id'), 'conversations', ['user_id'], unique=False)
    op.create_index(op.f('ix_conversations_session_id'), 'conversations', ['session_id'], unique=False)
    op.create_index(op.f('ix_conversations_id'), 'conversations', ['id'], unique=False)
    op.create_index(op.f('idx_session_created'), 'conversations', ['session_id', 'created_at'], unique=False)
    op.create_table('learning_sessions',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('session_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('level', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('duration_minutes', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('metrics', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), autoincrement=False, nullable=False),
    sa.Column('summary', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('learning_sessions_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('learning_sessions_pkey'))
    )
    op.create_index(op.f('ix_learning_sessions_user_id'), 'learning_sessions', ['user_id'], unique=False)
    op.create_index(op.f('ix_learning_sessions_session_date'), 'learning_sessions', ['session_date'], unique=False)
    op.create_table('exercise_results',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('session_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('exercise_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('exercise_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('user_answer', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('expected_answer', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('is_correct', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.Column('skill_tag', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('difficulty', sa.VARCHAR(), server_default=sa.text("'medium'::character varying"), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['learning_sessions.id'], name=op.f('exercise_results_session_id_fkey'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('exercise_results_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('exercise_results_pkey'))
    )
    op.create_index(op.f('ix_exercise_user_skill'), 'exercise_results', ['user_id', 'skill_tag'], unique=False)
    op.create_index(op.f('ix_exercise_user_created'), 'exercise_results', ['user_id', 'created_at'], unique=False)
    op.create_index(op.f('ix_exercise_session_created'), 'exercise_results', ['session_id', 'created_at'], unique=False)
    op.create_index(op.f('ix_exercise_results_user_id'), 'exercise_results', ['user_id'], unique=False)
    op.create_index(op.f('ix_exercise_results_skill_tag'), 'exercise_results', ['skill_tag'], unique=False)
    op.create_index(op.f('ix_exercise_results_session_id'), 'exercise_results', ['session_id'], unique=False)
    op.create_index(op.f('ix_exercise_results_exercise_type'), 'exercise_results', ['exercise_type'], unique=False)
    op.create_index(op.f('ix_exercise_results_created_at'), 'exercise_results', ['created_at'], unique=False)
    # ### end Alembic commands ###

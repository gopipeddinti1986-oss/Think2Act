"""milestone2 execution loop: planner, focus, productivity

Revision ID: 002_milestone2_execution_loop
Revises: 001_initial_schema
Create Date: 2026-09-01 01:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '002_milestone2_execution_loop'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. planner_entries table
    op.create_table(
        'planner_entries',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False),
        sa.Column('start_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='SCHEDULED'),
        sa.Column('source', sa.String(50), nullable=False, server_default='MANUAL'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    op.create_index('idx_planner_user_start', 'planner_entries', ['user_id', 'start_at'])
    op.create_index('idx_planner_user_id', 'planner_entries', ['user_id'])
    op.create_index('idx_planner_task_id', 'planner_entries', ['task_id'])

    # 2. focus_sessions table
    op.create_table(
        'focus_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='SET NULL'), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('productive_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('distracted_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('status', sa.String(50), nullable=False, server_default='RUNNING'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    op.create_index('idx_focus_user_started_at', 'focus_sessions', ['user_id', 'started_at'])
    op.create_index('idx_focus_user_id', 'focus_sessions', ['user_id'])

    # 3. productivity_metrics table
    op.create_table(
        'productivity_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('tasks_planned', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('tasks_completed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('focus_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('distraction_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('score', sa.Numeric(5, 2), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('user_id', 'date', name='uq_user_date_productivity')
    )
    op.create_index('idx_productivity_user_date', 'productivity_metrics', ['user_id', 'date'])

def downgrade() -> None:
    op.drop_table('productivity_metrics')
    op.drop_table('focus_sessions')
    op.drop_table('planner_entries')

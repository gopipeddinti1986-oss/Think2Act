"""add availability and activity events

Revision ID: 011_user_availability_and_activity
Revises: 010_settings_fields
Create Date: 2026-09-04 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '011_user_availability_and_activity'
down_revision: Union[str, None] = '010_settings_fields'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add availability & notification fields to user_profiles
    with op.batch_alter_table('user_profiles') as batch_op:
        batch_op.add_column(sa.Column('experience_level', sa.String(50), nullable=True, server_default='Entry'))
        batch_op.add_column(sa.Column('work_start_time', sa.String(10), nullable=True, server_default='09:00'))
        batch_op.add_column(sa.Column('work_end_time', sa.String(10), nullable=True, server_default='18:00'))
        batch_op.add_column(sa.Column('preferred_sprint_minutes', sa.Integer(), nullable=True, server_default='45'))
        batch_op.add_column(sa.Column('notification_preferences', sa.JSON(), nullable=True))

    # 2. Create activity_events table
    op.create_table(
        'activity_events',
        sa.Column('id', sa.Uuid(), primary_key=True),
        sa.Column('user_id', sa.Uuid(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('entity_type', sa.String(50), nullable=True),
        sa.Column('entity_id', sa.Uuid(), nullable=True),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('idx_activity_events_user_occurred', 'activity_events', ['user_id', 'occurred_at'])
    op.create_index('idx_activity_events_event_type', 'activity_events', ['event_type'])


def downgrade() -> None:
    op.drop_table('activity_events')
    with op.batch_alter_table('user_profiles') as batch_op:
        batch_op.drop_column('notification_preferences')
        batch_op.drop_column('preferred_sprint_minutes')
        batch_op.drop_column('work_end_time')
        batch_op.drop_column('work_start_time')
        batch_op.drop_column('experience_level')

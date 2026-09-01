"""milestone3 skills evidence history task_skills

Revision ID: 003_milestone3_skills
Revises: 002_milestone2_execution_loop
Create Date: 2026-09-01 02:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '003_milestone3_skills'
down_revision: Union[str, None] = '002_milestone2_execution_loop'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. skills table
    op.create_table(
        'skills',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    op.create_index('idx_skills_name', 'skills', ['name'], unique=True)

    # 2. user_skills table
    op.create_table(
        'user_skills',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False),
        sa.Column('level', sa.Numeric(5, 2), nullable=False, server_default='0.0'),
        sa.Column('confidence', sa.Numeric(5, 2), nullable=False, server_default='0.5'),
        sa.Column('last_assessed_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('user_id', 'skill_id', name='pk_user_skills')
    )
    op.create_index('idx_user_skills_user_id', 'user_skills', ['user_id'])
    op.create_index('idx_user_skills_skill_id', 'user_skills', ['skill_id'])

    # 3. evidence table
    op.create_table(
        'evidence',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False),
        sa.Column('source_type', sa.String(50), nullable=False),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('strength', sa.Numeric(5, 2), nullable=False, server_default='10.0'),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    op.create_index('idx_evidence_user_skill', 'evidence', ['user_id', 'skill_id'])

    # 4. skill_history table
    op.create_table(
        'skill_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False),
        sa.Column('level', sa.Numeric(5, 2), nullable=False),
        sa.Column('confidence', sa.Numeric(5, 2), nullable=False),
        sa.Column('reason', sa.String(255), nullable=True),
        sa.Column('recorded_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    op.create_index('idx_skill_history_user_skill', 'skill_history', ['user_id', 'skill_id', 'recorded_at'])

    # 5. task_skills table
    op.create_table(
        'task_skills',
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False),
        sa.PrimaryKeyConstraint('task_id', 'skill_id', name='pk_task_skills')
    )
    op.create_index('idx_task_skills_task_id', 'task_skills', ['task_id'])
    op.create_index('idx_task_skills_skill_id', 'task_skills', ['skill_id'])

def downgrade() -> None:
    op.drop_table('task_skills')
    op.drop_table('skill_history')
    op.drop_table('evidence')
    op.drop_table('user_skills')
    op.drop_table('skills')

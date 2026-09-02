"""milestone8 interview intelligence

Revision ID: 008_milestone8_interviews
Revises: 007_milestone7_resume
Create Date: 2026-09-02 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '008_milestone8_interviews'
down_revision: Union[str, None] = '007_milestone7_resume'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'interview_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role_title', sa.String(255), nullable=False),
        sa.Column('session_type', sa.String(50), nullable=False, server_default='TECHNICAL'),
        sa.Column('status', sa.String(50), nullable=False, server_default='IN_PROGRESS'),
        sa.Column('overall_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('summary_feedback', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('idx_interview_sessions_user_id', 'interview_sessions', ['user_id'])

    op.create_table(
        'interview_questions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('interview_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('target_skill', sa.String(100), nullable=True),
        sa.Column('difficulty', sa.String(50), nullable=False, server_default='MEDIUM'),
        sa.Column('user_answer', sa.Text(), nullable=True),
        sa.Column('rubric_scores', sa.JSON(), nullable=True),
        sa.Column('ai_feedback', sa.Text(), nullable=True),
        sa.Column('ideal_answer', sa.Text(), nullable=True),
        sa.Column('score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('interview_questions')
    op.drop_table('interview_sessions')

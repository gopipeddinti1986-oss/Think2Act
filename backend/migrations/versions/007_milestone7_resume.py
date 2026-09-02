"""milestone7 resume ats optimizer

Revision ID: 007_milestone7_resume
Revises: 006_milestone6_jobs
Create Date: 2026-09-02 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '007_milestone7_resume'
down_revision: Union[str, None] = '006_milestone6_jobs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'resumes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('target_role', sa.String(255), nullable=False),
        sa.Column('raw_text', sa.Text(), nullable=True),
        sa.Column('parsed_sections', sa.JSON(), nullable=True),
        sa.Column('ats_score', sa.Float(), nullable=True, server_default='70.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('idx_resumes_user_id', 'resumes', ['user_id'])

    op.create_table(
        'resume_suggestions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('resume_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('section', sa.String(100), nullable=False),
        sa.Column('suggestion_type', sa.String(50), nullable=False),
        sa.Column('current_text', sa.Text(), nullable=False),
        sa.Column('recommended_text', sa.Text(), nullable=False),
        sa.Column('impact_reason', sa.Text(), nullable=True),
        sa.Column('is_applied', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('resume_suggestions')
    op.drop_table('resumes')

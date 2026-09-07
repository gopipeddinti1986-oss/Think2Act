"""add settings fields to user_profiles

Revision ID: 010_settings_fields
Revises: 009_milestone9_decisions
Create Date: 2026-09-04 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '010_settings_fields'
down_revision: Union[str, None] = '009_milestone9_decisions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    with op.batch_alter_table('user_profiles') as batch_op:
        batch_op.add_column(sa.Column('target_role', sa.String(255), nullable=True))
        batch_op.add_column(sa.Column('target_companies', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('career_mode', sa.String(50), nullable=True, server_default='ACTIVE_SEARCH'))
        batch_op.add_column(sa.Column('github_handle', sa.String(100), nullable=True))
        batch_op.add_column(sa.Column('linkedin_profile_url', sa.String(255), nullable=True))
        batch_op.add_column(sa.Column('leetcode_username', sa.String(100), nullable=True))

    with op.batch_alter_table('tasks') as batch_op:
        batch_op.add_column(sa.Column('dependencies', sa.JSON(), nullable=True))

def downgrade() -> None:
    with op.batch_alter_table('tasks') as batch_op:
        batch_op.drop_column('dependencies')

    with op.batch_alter_table('user_profiles') as batch_op:
        batch_op.drop_column('leetcode_username')
        batch_op.drop_column('linkedin_profile_url')
        batch_op.drop_column('github_handle')
        batch_op.drop_column('career_mode')
        batch_op.drop_column('target_companies')
        batch_op.drop_column('target_role')

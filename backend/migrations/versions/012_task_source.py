"""add source column to tasks

Revision ID: 012_task_source
Revises: 011_user_availability_and_activity
Create Date: 2026-09-04 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '012_task_source'
down_revision: Union[str, None] = '011_user_availability_and_activity'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('tasks') as batch_op:
        batch_op.add_column(sa.Column('source', sa.String(50), nullable=True, server_default='USER'))


def downgrade() -> None:
    with op.batch_alter_table('tasks') as batch_op:
        batch_op.drop_column('source')

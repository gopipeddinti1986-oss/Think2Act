"""milestone4 learning intelligence: roles, role_skills, learning_resources, learning_paths

Revision ID: 004_milestone4_learning_intelligence
Revises: 003_milestone3_skills
Create Date: 2026-09-01 03:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '004_milestone4_learning_intelligence'
down_revision: Union[str, None] = '003_milestone3_skills'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. roles table
    op.create_table(
        'roles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    op.create_index('idx_roles_name', 'roles', ['name'], unique=True)

    # 2. role_skills table
    op.create_table(
        'role_skills',
        sa.Column('role_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False),
        sa.Column('required_level', sa.Numeric(5, 2), nullable=False, server_default='70.0'),
        sa.Column('importance', sa.String(50), nullable=False, server_default='HIGH'),
        sa.PrimaryKeyConstraint('role_id', 'skill_id', name='pk_role_skills')
    )
    op.create_index('idx_role_skills_role_id', 'role_skills', ['role_id'])
    op.create_index('idx_role_skills_skill_id', 'role_skills', ['skill_id'])

    # 3. learning_resources table
    op.create_table(
        'learning_resources',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('provider', sa.String(100), nullable=True),
        sa.Column('url', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.String(50), nullable=False, server_default='Intermediate'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )

    # 4. learning_resource_skills table
    op.create_table(
        'learning_resource_skills',
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('learning_resources.id', ondelete='CASCADE'), nullable=False),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False),
        sa.PrimaryKeyConstraint('resource_id', 'skill_id', name='pk_learning_resource_skills')
    )

    # 5. learning_paths table
    op.create_table(
        'learning_paths',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('goal_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('goals.id', ondelete='SET NULL'), nullable=True),
        sa.Column('role_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('roles.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    op.create_index('idx_learning_paths_user_id', 'learning_paths', ['user_id'])

    # 6. learning_path_items table
    op.create_table(
        'learning_path_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('learning_path_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('learning_paths.id', ondelete='CASCADE'), nullable=False),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), nullable=False),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('learning_resources.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('sequence_number', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.String(50), nullable=False, server_default='PENDING'),
        sa.Column('progress', sa.Numeric(5, 2), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    op.create_index('idx_learning_items_path_id', 'learning_path_items', ['learning_path_id'])

def downgrade() -> None:
    op.drop_table('learning_path_items')
    op.drop_table('learning_paths')
    op.drop_table('learning_resource_skills')
    op.drop_table('learning_resources')
    op.drop_table('role_skills')
    op.drop_table('roles')

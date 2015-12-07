"""Add users table

Revision ID: 157f3b3d9fb
Revises: 15f5bf79bb0
Create Date: 2015-12-07 15:17:04.451254

"""

# revision identifiers, used by Alembic.
revision = '157f3b3d9fb'
down_revision = '15f5bf79bb0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('users',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('email', sa.String(length=100), nullable=False),
                    sa.Column('password_hash', sa.String(length=80), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('is_admin', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('user_id'),
                    sa.UniqueConstraint('email'))


def downgrade():
    op.drop_table('users')

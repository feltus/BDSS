"""add destinations

Revision ID: 69bd02aad8ae
Revises: 54a47d983e4
Create Date: 2016-07-20 13:45:35.716875

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69bd02aad8ae'
down_revision = '54a47d983e4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('destinations',
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('last_updated_at', sa.DateTime(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('label', sa.String(length=100), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('created_by_user_id', sa.Integer(), nullable=False),
                    sa.Column('last_updated_by_user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['created_by_user_id'], ['users.user_id'], ),
                    sa.ForeignKeyConstraint(['last_updated_by_user_id'], ['users.user_id'], ),
                    sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_destinations_label'), 'destinations', ['label'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_destinations_label'), table_name='destinations')
    op.drop_table('destinations')

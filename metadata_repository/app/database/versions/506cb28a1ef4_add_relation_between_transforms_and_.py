"""add relation between transforms and destinations

Revision ID: 506cb28a1ef4
Revises: bc501eea2cfa
Create Date: 2016-07-21 19:40:44.387743

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '506cb28a1ef4'
down_revision = 'bc501eea2cfa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('transform_destinations',
                    sa.Column('transform_from_data_source_id', sa.Integer(), nullable=True),
                    sa.Column('transform_id', sa.Integer(), nullable=True),
                    sa.Column('destination_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['destination_id'], ['destinations.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['transform_from_data_source_id', 'transform_id'], ['url_transforms.from_data_source_id', 'url_transforms.transform_id'], ))


def downgrade():
    op.drop_table('transform_destinations')

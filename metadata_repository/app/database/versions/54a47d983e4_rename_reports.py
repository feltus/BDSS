"""Rename reports

Revision ID: 54a47d983e4
Revises: 400d8616184
Create Date: 2016-07-07 14:03:06.832297

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = '54a47d983e4'
down_revision = '400d8616184'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('timing_reports', 'transfer_reports')
    op.execute('ALTER INDEX "timing_reports_pkey" RENAME TO "transfer_reports_pkey"')
    op.execute('ALTER TABLE "transfer_reports" RENAME CONSTRAINT "timing_reports_data_source_id_fkey" TO "transfer_reports_data_source_id_fkey"')


def downgrade():
    op.rename_table('transfer_reports', 'timing_reports')
    op.execute('ALTER INDEX "transfer_reports_pkey" RENAME TO "timing_reports_pkey"')
    op.execute('ALTER TABLE "timing_reports" RENAME CONSTRAINT "transfer_reports_data_source_id_fkey" TO "timing_reports_data_source_id_fkey"')

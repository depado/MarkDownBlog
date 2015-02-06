"""empty message

Revision ID: 547b4a03fba
Revises: 9144c5cad
Create Date: 2015-02-05 10:02:38.674647

"""

# revision identifiers, used by Alembic.
revision = '547b4a03fba'
down_revision = '9144c5cad'

from alembic import op
import sqlalchemy as sa

from migrations.utils import drop_column_sqlite


def upgrade():
    op.add_column('user', sa.Column('blog_round_image', sa.Boolean(), nullable=True))


def downgrade():
    drop_column_sqlite('user', 'blog_round_image')

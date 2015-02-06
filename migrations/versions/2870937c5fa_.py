"""empty message

Revision ID: 2870937c5fa
Revises: 547b4a03fba
Create Date: 2015-02-06 14:21:20.794958

"""

# revision identifiers, used by Alembic.
revision = '2870937c5fa'
down_revision = '547b4a03fba'

from alembic import op
import sqlalchemy as sa

from migrations.utils import drop_column_sqlite


def upgrade():
    op.add_column('user', sa.Column('blog_bg', sa.String(length=200), nullable=True))
    op.add_column('user', sa.Column('blog_bg_everywhere', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('blog_bg_override', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('blog_bg_public', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('blog_bg_repeat', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('blog_image_rounded', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('last_login', sa.DateTime(), nullable=True))
    drop_column_sqlite('user', 'blog_round_image')


def downgrade():
    op.add_column('user', sa.Column('blog_round_image', sa.BOOLEAN(), nullable=True))
    drop_column_sqlite('user', 'last_login')
    drop_column_sqlite('user', 'blog_image_rounded')
    drop_column_sqlite('user', 'blog_bg_repeat')
    drop_column_sqlite('user', 'blog_bg_public')
    drop_column_sqlite('user', 'blog_bg_override')
    drop_column_sqlite('user', 'blog_bg_everywhere')
    drop_column_sqlite('user', 'blog_bg')

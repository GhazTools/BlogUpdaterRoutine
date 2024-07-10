"""Iniital Setup

Revision ID: 8cf256eaa4f5
Revises: 
Create Date: 2024-07-09 18:57:28.627111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cf256eaa4f5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_images',
    sa.Column('image_name', sa.String(), nullable=False),
    sa.Column('image_data', sa.LargeBinary(), nullable=False),
    sa.Column('released', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('image_name'),
    sa.UniqueConstraint('image_name')
    )
    op.create_table('blog_posts',
    sa.Column('post_name', sa.String(length=256), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('released', sa.Boolean(), nullable=False),
    sa.Column('release_date', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('post_name'),
    sa.UniqueConstraint('post_name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_posts')
    op.drop_table('blog_images')
    # ### end Alembic commands ###
"""Initial migration

Revision ID: 44c45a4753b3
Revises: 
Create Date: 2023-12-08 12:50:34.150925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44c45a4753b3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contact_info')
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email1', sa.String(length=120), nullable=False))
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=120), nullable=False))
        batch_op.drop_column('email1')

    op.create_table('contact_info',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('phone', sa.VARCHAR(length=20), nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), nullable=True),
    sa.Column('address', sa.VARCHAR(length=255), nullable=True),
    sa.Column('freelance_available', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

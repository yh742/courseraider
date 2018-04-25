"""empty message

Revision ID: 0cbaf50bad45
Revises: ad7ec4e9e455
Create Date: 2018-04-25 16:30:50.070884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cbaf50bad45'
down_revision = 'ad7ec4e9e455'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classes_date'), 'classes', ['date'], unique=False)
    op.create_index(op.f('ix_classes_title'), 'classes', ['title'], unique=False)
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qnum', sa.Integer(), nullable=True),
    sa.Column('widget', sa.String(length=128), nullable=True),
    sa.Column('jtype', sa.String(length=256), nullable=True),
    sa.Column('title', sa.String(length=1028), nullable=True),
    sa.Column('extra', sa.String(length=256), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('performances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('performances')
    op.drop_table('questions')
    op.drop_index(op.f('ix_classes_title'), table_name='classes')
    op.drop_index(op.f('ix_classes_date'), table_name='classes')
    op.drop_table('classes')
    # ### end Alembic commands ###

"""empty message

Revision ID: 556aecd77b76
Revises: c40383fe88fc
Create Date: 2018-08-28 13:09:54.436564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '556aecd77b76'
down_revision = 'c40383fe88fc'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('made_recipes',
		sa.Column('user_id', sa.Integer(), nullable=False),
		sa.Column('recipe_id', sa.Integer(), nullable=False),
		sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
		sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
		sa.PrimaryKeyConstraint('user_id', 'recipe_id')
	)


def downgrade():
	op.drop_table('made_recipes')

"""empty message

Revision ID: d81fc86bc06d
Revises: 7cdf7c412aef
Create Date: 2022-04-04 22:10:24.365168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd81fc86bc06d'
down_revision = '7cdf7c412aef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Artist', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('Artist', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('website', sa.String(length=120), nullable=True))
    op.alter_column('Artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=False))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.add_column('Venue', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'past_shows_count')
    op.drop_column('Venue', 'upcoming_shows_count')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'genres')
    op.alter_column('Artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_column('Artist', 'website')
    op.drop_column('Artist', 'past_shows_count')
    op.drop_column('Artist', 'upcoming_shows_count')
    op.drop_column('Artist', 'seeking_description')
    op.drop_column('Artist', 'seeking_talent')
    op.drop_table('shows')
    # ### end Alembic commands ###

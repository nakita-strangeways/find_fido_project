"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import Animal
from model import Color
from model import AnimalColor
from model import Species
from model import Breed
# from model import User


from model import connect_to_db, db
from server import app
import datetime


def load_colors():
    """Load users from u.user into database."""

    print("Colors")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Color.query.delete()

    #Read generic_colors file and insert data
    for row in open("seed_data/generic_colors"):
        row = row.rstrip()
        color_id, color = row.split("|")

    colors = Color(color_id=color_id,
                    color=color)

    # We need to add to the session or it won't ever be stored
    db.session.add(colors)

    # Once we're done, we should commit our work
    db.session.commit()


def load_species():
    """Load users from u.user into database."""

    print("Species")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Species.query.delete()

    #Read species file and insert data
    for row in open("seed_data/species"):
        row = row.rstrip()
        species_id, species = row.split("|")

    the_species = Species(species_id=species_id,
                    species=species)

    # We need to add to the session or it won't ever be stored
    db.session.add(the_species)

    # Once we're done, we should commit our work
    db.session.commit()


def load_sizes():
    """Load users from u.user into database."""

    print("Sizes")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Size.query.delete()

    #Read sizes file and insert data
    for row in open("seed_data/sizes"):
        row = row.rstrip()
        size_id, size = row.split("|")

    sizes = Size(size_id=size_id,
                    size=size)

    # We need to add to the session or it won't ever be stored
    db.session.add(sizes)

    # Once we're done, we should commit our work
    db.session.commit()

def load_breeds():
    """Load users from u.user into database."""

    print("Breeds")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Breed.query.delete()

    #Read sizes file and insert data
    for row in open("seed_data/all_breeds"):
        row = row.rstrip()
        species_id, breed = row.split("|")

    breeds = Breeds(species_id=species_id,
                    breed=breed)

    # We need to add to the session or it won't ever be stored
    db.session.add(breeds)

    # Once we're done, we should commit our work
    db.session.commit()






# if __name__ == "__main__":
#     connect_to_db(app)

#     # In case tables haven't been created, create them
#     db.create_all()

#     # Import different types of data
#     load_users()
#     load_movies()
#     load_ratings()
#     set_val_user_id()
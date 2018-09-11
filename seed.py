"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import Animal, Color, AnimalColor, Species, Size, Breed, connect_to_db, db
from server import app


# ADD LATER: from model import User

def load_colors(color_filename):
    """Load colors from seed_data/generic_colors into database."""

    print("Colors")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Color.query.delete()

    #Read generic_colors file and insert data
    for row in open(color_filename):
        row = row.rstrip()
        color_id, color = row.split("|")

        colors = Color(color_id=color_id,
                        color=color)

        # We need to add to the session or it won't ever be stored
        db.session.add(colors)

    # Once we're done, we should commit our work
    db.session.commit()


def load_species(species_filename):
    """Load species from seed_data/species into database."""

    print("Species")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Species.query.delete()

    #Read species file and insert data
    for row in open(species_filename):
        row = row.rstrip()
        species_id, species = row.split("|")

        the_species = Species(species_id=species_id,
                    species=species)

        # We need to add to the session or it won't ever be stored
        db.session.add(the_species)

    # Once we're done, we should commit our work
    db.session.commit()


def load_sizes(sizes_filename):
    """Load sizes from seed_data/sizes into database."""

    print("Sizes")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    # BROKEN?
    Size.query.delete()

    #Read sizes file and insert data
    for row in open(sizes_filename):
        row = row.rstrip()
        size_id, size = row.split("|")

        sizes = Size(size_id=size_id,
                    size=size)

        # We need to add to the session or it won't ever be stored
        db.session.add(sizes)

    # Once we're done, we should commit our work
    db.session.commit()

def load_breeds(breeds_filename):
    """Load breeds from seed_data/all_breeds into database."""

    print("Breeds")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Breed.query.delete()

    #Read sizes file and insert data
    for row in open(breeds_filename):
        row = row.rstrip()
        species_id, breed = row.split("|")

        breeds = Breed(species_id=species_id,
                    breed=breed)

        # We need to add to the session or it won't ever be stored
        db.session.add(breeds)

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    color_filename = "seed_data/generic_colors"
    species_filename = "seed_data/sizes"
    sizes_filename = "seed_data/sizes"
    breeds_filename  = "seed_data/all_breeds"

    load_colors(color_filename)
    load_species(species_filename)
    load_sizes(sizes_filename)
    load_breeds(breeds_filename)
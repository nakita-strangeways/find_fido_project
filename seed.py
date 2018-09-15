"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import Animal, Color, AnimalColor, Species, Size, Breed, connect_to_db, db
from server import app


# ADD LATER: from model import User

def load_colors(color_filename):
    """Load colors from seed_data/generic_colors into database."""

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

    #finished the function
    print("Colors inserted")


def load_species(species_filename):
    """Load species from seed_data/species into database."""

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

    #finished the function
    print("Species inserted")


def load_sizes(sizes_filename):
    """Load sizes from seed_data/sizes into database."""


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

    #finished the function
    print("Sizes inserted")

def load_breeds(breeds_filename):
    """Load breeds from seed_data/all_breeds into database."""

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

    #finished the function
    print("Breeds inserted")

def load_animals(animal_filename):
    """Load colors from seed_data/generic_colors into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Animal.query.delete()

    #Read generic_colors file and insert data
    for row in open(animal_filename):
        row = row.rstrip()
        animal_id, species_id, breed_id, size_id, user_id, seen_at_lat, seen_at_long, timestamp, photo, notes = row.split("|")

        animals = Animal(animal_id=animal_id,
                        species_id=species_id,
                        breed_id=breed_id,
                        size_id=size_id,
                        user_id=user_id,
                        seen_at_lat=seen_at_lat,
                        seen_at_long=seen_at_long,
                        timestamp_seen_at=timestamp,
                        photo=photo,
                        notes=notes)

        # We need to add to the session or it won't ever be stored
        db.session.add(animals)

    # Once we're done, we should commit our work
    db.session.commit()

    #finished the function
    print("Animals inserted")


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    animal_filename = "seed_data/lost_pets_data"
    color_filename = "seed_data/generic_colors"
    species_filename = "seed_data/species"
    sizes_filename = "seed_data/sizes"
    breeds_filename  = "seed_data/all_breeds"

    load_colors(color_filename)
    load_species(species_filename)
    load_sizes(sizes_filename)
    load_breeds(breeds_filename)
    load_animals(animal_filename)
"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import Animal, Color, AnimalColor, Species, Size, Breed, User, connect_to_db, db #add userAnimal?
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

        colors = Color(color=color)

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

        the_species = Species(species=species)

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

        sizes = Size(size=size)

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

def load_users(users_filename):
    """Load load_users from seed_data/load_users into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    #Read load_users file and insert data
    for row in open(users_filename):
        row = row.rstrip()
        username, email, password, f_name, l_name = row.split("|")

        users = User(username=username,
                        email=email,
                        password=password,
                        f_name=f_name,
                        l_name=l_name)

        # We need to add to the session or it won't ever be stored
        db.session.add(users)

    # Once we're done, we should commit our work
    db.session.commit()

    #finished the function
    print("Users inserted")


def load_animals(animal_filename):
    """Load colors from seed_data/generic_colors into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Animal.query.delete()

    #Read generic_colors file and insert data
    for row in open(animal_filename):
        row = row.rstrip()
        animal_id, species_id, breed_id, size_id, user_id, latitude, longitude, timestamp, photo, notes, found, found_by_user_id = row.split("|")

        if found_by_user_id == "None":
            found_by_user_id = None

        animals = Animal(species_id=species_id,
                        breed_id=breed_id,
                        size_id=size_id,
                        user_id=user_id,
                        latitude=latitude,
                        longitude=longitude,
                        timestamp=timestamp,
                        photo=photo,
                        notes=notes,
                        found=bool(found),
                        found_by_user_id = found_by_user_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(animals)

    # Once we're done, we should commit our work
    db.session.commit()

    #finished the function
    print("Animals inserted")


def load_animalColors(animalColors_filename):
    """Load animalColors from seed_data/animalColors into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    AnimalColor.query.delete()

    #Read animalColors file and insert data
    for row in open(animalColors_filename):
        row = row.rstrip()
        animal_color_id, animal_id, color_id = row.split("|")

        animalColors = AnimalColor(animal_id=animal_id,
                                        color_id=color_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(animalColors)

    # Once we're done, we should commit our work
    db.session.commit()

    #finished the function
    print("Animal Colors inserted")

# def load_userAnimals(userAnimals_filename):
#     """Load userAnimals from seed_data/userAnimals into database."""

#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     UserAnimal.query.delete()

#     #Read animalColors file and insert data
#     for row in open(userAnimals_filename):
#         row = row.rstrip()
#         user_animals_id, animal_id, user_id = row.split("|")

#         userAnimals = userAnimals(animal_id=animal_id,
#                                         user_id=user_id)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(userAnimals)

#     # Once we're done, we should commit our work
#     db.session.commit()

#     #finished the function
#     print("User Animals inserted")




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
    animalColors_filename = "seed_data/animalColors"
    users_filename = "seed_data/users"
    # userAnimals_filename = "seed_data/userAnimals"

    load_colors(color_filename)
    load_species(species_filename)
    load_sizes(sizes_filename)
    load_breeds(breeds_filename)
    load_users(users_filename)
    load_animals(animal_filename)
    load_animalColors(animalColors_filename)
    # load_userAnimals(userAnimals_filename)

"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import Animal, Color, AnimalColor, Species, Size, Breed, Gender, User, Lost_Pet_Submission, lostPetColor, connect_to_db, db #add userAnimal?
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

def load_genders(genders_filename):
    """Load breeds from seed_data/all_breeds into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Gender.query.delete()

    #Read sizes file and insert data
    for row in open(genders_filename):
        row = row.rstrip()
        gender_id, gender = row.split("|")

        genders = Gender(gender_id=gender_id,
                    gender=gender)

        # We need to add to the session or it won't ever be stored
        db.session.add(genders)

    # Once we're done, we should commit our work
    db.session.commit()

    #finished the function
    print("Genders inserted")

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
        animal_id, species_id, breed_id, size_id, user_id, latitude, longitude, timestamp, photo, notes, found, found_by_user_id, gender_id = row.split("|")

        if found_by_user_id == "None":
            found_by_user_id = None
            
        if found == "True":
            found = True
        else:
            found = False

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
                        found_by_user_id = found_by_user_id,
                        gender_id = gender_id)

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

def load_lostPetPosters(lostPet_filename):
    """Loads lost animals into lost_pet_posters table."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Lost_Pet_Submission.query.delete()

    #Read animalColors file and insert data
    for row in open(lostPet_filename):
        row = row.rstrip()
        pet_id, species_id, breed_id, user_id, pet_name, latitude, longitude, date_lost, photo, notes, gender_id = row.split("|")

        lost_Pet_Submissions = Lost_Pet_Submission(species_id=species_id,
                                                    breed_id=breed_id,
                                                    user_id=user_id,
                                                    pet_name=pet_name,
                                                    latitude=latitude,
                                                    longitude=longitude,
                                                    date_lost=date_lost,
                                                    photo=photo,
                                                    notes=notes,
                                                    gender_id=gender_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(lost_Pet_Submissions)

    # Once we're done, we should commit our work
    db.session.commit()

    #finished the function
    print("lost pets inserted")

def load_lostPetColors(lostPetColors_filename):
    """Load lostPetColors from seed_data/lostPetColors into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    lostPetColor.query.delete()

    #Read lostPetColor file and insert data
    for row in open(lostPetColors_filename):
        row = row.rstrip()
        animal_color_id, pet_id, color_id = row.split("|")

        lostPetColors = lostPetColor(pet_id=pet_id,
                                        color_id=color_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(lostPetColors)

    # Once we're done, we should commit our work
    db.session.commit()

    #finished the function
    print("lostPet Colors inserted")



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
    genders_filename = "seed_data/gender"
    animalColors_filename = "seed_data/animalColors"
    users_filename = "seed_data/users"
    lostPet_filename = "seed_data/lost_pet_posters_data"
    lostPetColors_filename = "seed_data/lostPetColors_data"

    load_colors(color_filename)
    load_species(species_filename)
    load_sizes(sizes_filename)
    load_breeds(breeds_filename)
    load_genders(genders_filename)
    load_users(users_filename)
    load_animals(animal_filename)
    load_animalColors(animalColors_filename)
    load_lostPetPosters(lostPet_filename)
    load_lostPetColors(lostPetColors_filename)


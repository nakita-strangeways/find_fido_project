"""Models and database functions for Find_Fido project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Animal(db.Model):
    """Animals seen submitted by users."""

    __tablename__ = "animals"

    animal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    species_id = db.Column(db.Integer, 
                        db.ForeignKey('species.species_id'),
                        nullable=False)
    breed_id = db.Column(db.Integer, 
                        db.ForeignKey('breeds.breed_id'),
                        nullable=True)
    size_id = db.Column(db.Integer, 
                        db.ForeignKey('sizes.size_id'),
                        nullable=False)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'),
                        nullable=False) 
    latitude = db.Column(db.String(20), nullable=False)
    longitude = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    photo = db.Column(db.String(64), nullable=False)
    notes = db.Column(db.String(150), nullable=False)
    found = db.Column(db.Boolean, server_default='f', default=False, nullable=False)
    found_by_user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'))

    colors = db.relationship("Color",
                            secondary="animal_colors",
                            backref="animals")





    breed = db.relationship("Breed")
    species = db.relationship("Species")
    size = db.relationship("Size")
    user = db.relationship("User", foreign_keys = [user_id])
    found_user = db.relationship("User", foreign_keys = [found_by_user_id])



    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Animal animal_id={self.animal_id} species_id={self.species_id}>"

class Color(db.Model):
    """Color options of animals."""

    __tablename__ = "colors"

    color_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    color = db.Column(db.String(30), nullable=False)

    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Color color_id={self.color_id} color={self.color}>"

class AnimalColor(db.Model):
    """An associations table between animals table and colors table."""

    __tablename__ = "animal_colors"

    animal_color_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    animal_id = db.Column(db.Integer, 
                        db.ForeignKey('animals.animal_id'),
                        nullable=False)
    color_id = db.Column(db.Integer, 
                        db.ForeignKey('colors.color_id'),
                        nullable=False)

    animals = db.relationship("Animal")
    colors = db.relationship("Color")
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<AnimalColor animal_color_id={self.animal_color_id} \
                        color_id={self.color_id} animal_id={self.animal_id}>"


class Species(db.Model):
    """Species options of animals."""

    __tablename__ = "species"

    species_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    species = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Species species_id={self.species_id} species={self.species}>"

class Breed(db.Model):
    """Size options of animals."""

    __tablename__ = "breeds"

    breed_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    breed = db.Column(db.String(64), nullable=False)
    species_id = db.Column(db.Integer, 
                        db.ForeignKey('species.species_id'),
                        nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Breed breed_id={self.breed_id} breed={self.breed} species_id={self.species_id}>"


class Size(db.Model):
    """Size options of animals."""

    __tablename__ = "sizes"

    size_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    size = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Size size_id={self.size_id} size={self.size}>"


class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    f_name = db.Column(db.String(64), nullable=True)
    l_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email} password={self.password} username={self.username} f_name={self.f_name} l_name={self.l_name}>"

class Lost_Pet_Submission(db.Model):
    """Owners submit lost pets"""

    __tablename__ = "lost_pet_posters"

    pet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    species_id = db.Column(db.Integer, 
                        db.ForeignKey('species.species_id'),
                        nullable=False)
    breed_id = db.Column(db.Integer, 
                        db.ForeignKey('breeds.breed_id'),
                        nullable=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    pet_name = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.String(20), nullable=False)
    longitude = db.Column(db.String(20), nullable=False)
    date_lost = db.Column(db.String(64), nullable=False)
    photo = db.Column(db.String(64), nullable=False)
    notes = db.Column(db.String(150), nullable=False)

    colors = db.relationship("Color",
                            secondary="lostPet_colors",
                            backref="lost_pet_posters")

    breed = db.relationship("Breed")
    species = db.relationship("Species")
    user = db.relationship("User", foreign_keys = [user_id])

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Lost_Pet_Submission pet_id={self.pet_id} species_id={self.species_id}>"

class lostPetColor(db.Model):
    """An associations table between lost_pet_posters table and colors table."""

    __tablename__ = "lostPet_colors"

    animal_color_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pet_id = db.Column(db.Integer, 
                        db.ForeignKey('lost_pet_posters.pet_id'),
                        nullable=False)
    color_id = db.Column(db.Integer, 
                        db.ForeignKey('colors.color_id'),
                        nullable=False)

    lost_pets = db.relationship("Lost_Pet_Submission")
    colors = db.relationship("Color")
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<lostPetColor lostPet_color_id={self.animal_color_id} \
                        color_id={self.color_id} pet_id={self.pet_id}>"



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///animals'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
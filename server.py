from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import Animal, Color, AnimalColor, Species, Breed, Size, connect_to_db, db

from datetime import datetime, date, time


app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')

@app.route('/lost')
def map():
    """Show map of lost pets."""

    colors = db.session.query(Color)
    breeds = db.session.query(Breed)

    return render_template("pet_map.html", 
                                    colors=colors,
                                    breeds=breeds)

@app.route('/lost.json')
def lost_pet_info():
    """JSON information about lost pets from lost_pets_data file."""

    lost = {
        animal.animal_id: {
            "animal_id": animal.animal_id,
            "species_id": animal.species.species,
            "size_id": animal.size.size,
            "latitude": animal.latitude,
            "longitude": animal.longitude,
            "timestamp": animal.timestamp,
            "photo": animal.photo,
            "notes": animal.notes
        }

        for animal in Animal.query
    }

    return jsonify(lost)


@app.route('/add_lost_animal', methods=['POST'])
def lost_pet_form(): 
    """Adds a lost pet."""

    submitted_species = request.form.get('species')
    submitted_breed = request.form.get('breed')
    submitted_size = request.form.get('size')
    # submitted_color1 = request.form.get('color1_quest')
    # submitted_color2 = request.form.get('color2_quest')
    # submitted_color3 = request.form.get('color3_quest')
    submitted_notes = request.form.get('notes')
    submitted_photo = request.form.get('photo')
    submitted_latitude = request.form.get('lat')
    submitted_longitude = request.form.get('lng')
    submitted_email = request.form.get('email')

    timestamp = datetime.now()


    species_id = Species.query.filter(Species.species == submitted_species).one()
    breed_id = Breed.query.filter(Breed.breed == submitted_breed).one()
    size_id = Size.query.filter(Size.size == submitted_size).one()

    animal = Animal(species_id = species_id,
                     breed_id = breed_id,
                     size_id = size_id, 
                     notes = submitted_notes, 
                     photo = submitted_photo, 
                     latitude = submitted_latitude, 
                     longitude = submitted_longitude, 
                     user_id = submitted_email, 
                     timestamp = timestamp)

    db.session.add(animal)
    db.session.commit()
    print("committed")

    # print(submitted_species, submitted_breed, submitted_size, submitted_notes,submitted_photo,submitted_latitude,submitted_longitude,submitted_email,timestamp, species_id, breed_id, size_id)


    # return render_template('testing.html', species = submitted_species,
    #                                     breed = submitted_breed,
    #                                     size = submitted_size,
    #                                     notes = submitted_notes,
    #                                     photo = submitted_photo,
    #                                     latitude = submitted_latitude,
    #                                     longitude = submitted_longitude,
    #                                     email = submitted_email,
    #                                     timestamp = timestamp,
    #                                     species_id = species_id,
    #                                     breed_id = breed_id,
    #                                     size_id = size_id)

# @app.route('/test')
# def testing():
#     """Homepage."""

#     return render_template('testing.html')


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import Animal, Color, AnimalColor, Species, Breed, Size, connect_to_db, db


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
            "seen_at_lat": animal.seen_at_lat,
            "seen_at_long": animal.seen_at_long,
            "timestamp_seen_at": animal.timestamp_seen_at,
            "photo": animal.photo,
            "notes": animal.notes
        }

        for animal in Animal.query
    }

    return jsonify(lost)


@app.route('/lost', methods=['POST'])
def lost_pet_form(): 
    """Adds a lost pet."""

    species = request.form.get('species_quest')
    breed = request.form.get('breed_quest')
    size = request.form.get('size_quest')
    color1 = request.form.get('color1_quest')
    color2 = request.form.get('color2_quest')
    color3 = request.form.get('color3_quest')
    notes = request.form.get('notes')
    picture = request.form.get('animal_pic')
    address = request.form.get('loc_quest')


    # model.make_new_student(first_name, last_name, github)

    # session["added_student"] = {'first_name': first_name,
    #                            'last_name': last_name,
    #                            'github': github}

    # html = render_template('student_add.html', first=first_name, last=last_name, github=github)

    return html

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
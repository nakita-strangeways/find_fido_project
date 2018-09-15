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

    return render_template("pet_map.html")

@app.route('/lost.json')
def bear_info():
    """JSON information about lost pets from lost_pets_data file."""

    lost = {
        animal.animal_id: {
            "animal_id": animal.animal_id,
            "species": animal.species_id,
            "size": animal.size_id,
            "seen_at_lat": animal.seen_at_lat,
            "seen_at_long": animal.seen_at_long,
            "timestamp_seen_at": animal.timestamp_seen_at,
            "photo": animal.photo,
            "notes": animal.notes
        }

        for animal in Animal.query}

    return jsonify(lost)
    


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
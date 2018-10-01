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
            "notes": animal.notes,
            "colors": [color.color for color in animal.colors]
        }

        for animal in Animal.query

    }

    return jsonify(lost)


@app.route('/add_lost_animal', methods=['POST'])
def lost_pet_form(): 
    """Adds a lost pet."""
    colors = []
    queried_colors = []

    f = request.files['animal_photo']
    f.save('static/seed_photos/' + f.filename)

    submitted_species = request.form.get('species_quest')
    submitted_breed = request.form.get('breed_question')
    submitted_size = request.form.get('size_quest')
    submitted_color1 = request.form.get('color1_question')
    if submitted_color1:
        print(submitted_color1)
        colors.append(submitted_color1)
    submitted_color2 = request.form.get('color2_question')
    if submitted_color2:    
        colors.append(submitted_color2)
    submitted_color3 = request.form.get('color3_question')
    if submitted_color3:
        colors.append(submitted_color3)
    submitted_notes = request.form.get('notes')
    submitted_latitude = request.form.get('lat')
    submitted_longitude = request.form.get('lng')
    submitted_email = request.form.get('email')
    timestamp = datetime.now()

    # print(f)
    # print(request.form)
    # print(submitted_latitude)

    species = Species.query.filter(Species.species == submitted_species).one()
    breed = Breed.query.filter(Breed.breed == submitted_breed).one()
    size = Size.query.filter(Size.size == submitted_size).one()
    for color in colors:
        queried_colors.append(Color.query.filter(Color.color == color).one())


    animal = Animal(species = species,
                     breed = breed,
                     size = size, 
                     notes = submitted_notes, 
                     photo = str(f.filename),
                     latitude = submitted_latitude, 
                     longitude = submitted_longitude, 
                     user_id = submitted_email, 
                     timestamp = timestamp,
                     colors = queried_colors
                     )

    db.session.add(animal)
    db.session.commit()
    return("it worked. yay")



#FIIIIX THIS IMAGE THIIIING
@app.route('/images/<int:animal_id>.jpg')
def get_image(animal_id):
    image_binary = read_image(animal_id)
    return send_file(
        io.BytesIO(image_binary),
        mimetype='image/jpeg',
        as_attachment=True,
        attachment_filename='%s.jpg' % animal_id)





if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
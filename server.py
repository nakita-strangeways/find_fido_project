from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension


from model import Animal, Color, AnimalColor, Species, Breed, Size, User, connect_to_db, db

from datetime import datetime, date, time


app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    colors = db.session.query(Color)
    breeds = db.session.query(Breed)

    return render_template("homepage.html", 
                                    colors=colors,
                                    breeds=breeds
                                    )

@app.route('/.json')
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
            "colors": [color.color for color in animal.colors],
            "user_id": animal.user.username,
            "found": animal.found,
            "found_by_user_id": animal.user.username
        }
        for animal in Animal.query
    }
    return jsonify(lost)

@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == email).one()

    if not user:
        flash("No such email address.")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password.")
        return redirect("/login")

    session["logged_in_user_email"] = user.email
    flash("Logged in.")
    return redirect("/")


@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["logged_in_user_email"]
    flash("Logged out.")
    return redirect("/")


@app.route("/create_user", methods=["GET"])
def show_create_user():
    """Show create_user form."""

    return render_template("create_user.html")

@app.route("/profile")
def show_user_profile():
    """Show user profile."""

    return render_template("profile.html")


@app.route('/create_user', methods=['POST'])
def create_user_form(): 
    """Adds a new user."""

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    new_user = User(username = username,
                    email = email,
                    password = password)

    db.session.add(new_user)
    db.session.commit()
    print("submitted new user to database!")
    flash("Account Created! Please sign in.")
    return redirect("/login")

@app.route('/add_lost_animal', methods=['POST'])
def lost_pet_form(): 
    """Adds a lost pet."""
    colors = []
    queried_colors = []
    queried_breed = []

    f = request.files['animal_photo']
    f.save('static/seed_photos/' + f.filename)

    submitted_species = request.form.get('species_quest')
    submitted_breed = request.form.get('breed_question')
    if submitted_breed:
        submitted_breed = submitted_breed
    else:
        submitted_breed = 'Unknown'
    submitted_size = request.form.get('size_quest')
    submitted_color1 = request.form.get('color1_question')
    if submitted_color1:
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
    timestamp = datetime.now()
    user_email = session.get('logged_in_user_email')


    species = Species.query.filter(Species.species == submitted_species).one()
    # breed = Breed.query.filter(Breed.breed == submitted_breed).one()
    size = Size.query.filter(Size.size == submitted_size).one()
    for color in colors:
        queried_colors.append(Color.query.filter(Color.color == color).one())

    breed = Breed.query.filter(Breed.breed == submitted_breed,
                                 Breed.species_id == species.species_id).one()

    user = User.query.filter(User.email == user_email).one()

    animal = Animal(species = species,
                    breed = breed,
                    size = size, 
                    notes = submitted_notes, 
                    photo = str(f.filename),
                    latitude = submitted_latitude, 
                    longitude = submitted_longitude, 
                    user_id = user.user_id, 
                    timestamp = timestamp,
                    colors = queried_colors
                    )

    db.session.add(animal)
    db.session.commit()
    print("submitted lost animal to database!")
    return("it worked. yay")


# DO I NEED THIS?
# @app.route('/found_animal', methods=['POST'])
# def found_animal_update(): 
#     """Updates animal columns Found = True, along with user who submitted found."""

#     user_email = session.get('logged_in_user_email')

#     animal = Animal(found = True,
#                     breed = breed,
#                     )    

#     db.session.add(animal)
#     db.session.commit()
#     print("submitted lost animal to database!")
#     return("it worked. yay")

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
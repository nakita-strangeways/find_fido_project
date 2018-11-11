from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension


from model import Animal, Color, AnimalColor, Species, Breed, Size, User, Lost_Pet_Submission, lostPetColor, connect_to_db, db

from datetime import datetime, date, time


app = Flask(__name__)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    colors = db.session.query(Color)
    breeds = db.session.query(Breed)
    animals = db.session.query(Animal)

    return render_template("homepage.html", 
                                    colors=colors,
                                    breeds=breeds,
                                    animals=animals
                                    )

@app.route('/.json')
def lost_pet_info():
    """JSON information about seen animals from lost_pets_data file."""

    lost = {
        animal.animal_id: {
            "animal_id": animal.animal_id,
            "species_id": animal.species.species,
            "breed_id": animal.breed.breed, 
            "size_id": animal.size.size,
            "latitude": animal.latitude,
            "longitude": animal.longitude,
            "timestamp": animal.timestamp,
            "photo": animal.photo,
            "notes": animal.notes,
            "colors": [color.color for color in animal.colors],
            "user_id": animal.user.username,
            "found": animal.found,
            "found_by_user_id": animal.found_user.username if animal.found_user else None
        }
        for animal in Animal.query
    }
    return jsonify(lost)

@app.route('/lost_pet_posters.json')
def missing_pet_poster_info():
    """JSON information about seen animals from lost_pets_data file."""

    missing_pet = {
        pet.pet_id: {
            "pet_id": pet.pet_id,
            "species_id": pet.species.species,
            "breed_id": pet.breed.breed,
            "user_id": pet.user.username,
            "pet_name": pet.pet_name,
            "latitude": pet.latitude,
            "longitude": pet.longitude,
            "date_lost": pet.date_lost,
            "photo": pet.photo,
            "notes": pet.notes,
            "colors": [color.color for color in pet.colors],

        }
        for pet in Lost_Pet_Submission.query
    }
    return jsonify(missing_pet)

@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == email).first()

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

    if session.get("logged_in_user_email") == None:
        flash("Please sign in to go to your profile page")
        return render_template("login.html")

    else:
        user_email = session.get('logged_in_user_email')

        user = User.query.filter(User.email == user_email).one()

        return render_template("profile.html",
                                    user=user)

@app.route('/change_password', methods=['POST'])
def change_password_form(): 
    """Changes users password."""

    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    repeat_new_password = request.form.get('repeat_new_password')

    user_email = session.get('logged_in_user_email')
    print(user_email)

    found_user_id = User.query.filter(User.email == user_email).one()
    print(found_user_id)

    #if passwords dont match - this errors. Need to fix.
    found_user_password = User.query.filter(User.password == old_password).first()

    if found_user_password == None:
        flash("Old password doesn't match. Please try again")
        return redirect('/profile') 

    else:
        if old_password == found_user_password.password:
            print("They match")
            if new_password == repeat_new_password:
                print("both new passwords match")
                found_user_password.password = new_password

                db.session.commit()

            else:
                flash("New passwords don't match. Please try again")
                return redirect('/profile')

    flash("Password has been changed!")
    return redirect("/profile")


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
    flash("Lost animal has been added to map!")
    return("it worked. yay")

@app.route('/found_animal', methods=['POST'])
def found_animal_update(): 
    """Updates animal columns Found = True, along with user who submitted found."""

    user_email = session.get('logged_in_user_email')
    print(user_email)
    
    found_animal_id = int(request.json.get("found_animal_id"))

    found_user_id = User.query.filter(User.email == user_email).one()
    print(found_user_id)

    animal_found = Animal.query.filter(Animal.animal_id == found_animal_id).one()


    animal_found.found = True
    animal_found.found_by_user_id = found_user_id.user_id

    db.session.commit()

    print("changed found to True in animal table!")
    flash("Animal has been marked as returned home.")
    return("it worked. yay")

@app.route('/lost_pet_posters')
def lost_pet_posters_page():
    """shows all the lost pet pages."""

    colors = db.session.query(Color)
    breeds = db.session.query(Breed)
    lost_pets = db.session.query(Lost_Pet_Submission)


    return render_template("lost_pet_poster_page.html", 
                                    colors=colors,
                                    breeds=breeds,
                                    lost_pets=lost_pets
                                    )

@app.route('/lost_pet_posters_searchbox', methods=['POST'])
def lost_pet_posters_searchbox():
    """."""

    print(request.form)

    searched_species = int(request.form.get('PetType'))
    searched_zipcode = request.form.get('Zipcode')
    searched_name_or_id = request.form.get('SearchByNameID')
    searched_breed = request.form.get('SearchByBreed')
    searched_color = request.form.get('SearchByColor')

    print(searched_zipcode)
    print(searched_name_or_id)
    print(searched_species)
    print(searched_breed)
    print(searched_color)


    query = Lost_Pet_Submission.query

# Working
    if searched_species:
        query = query.filter(Lost_Pet_Submission.species_id == searched_species)

## Working
    if searched_breed:
        breed_id = Breed.query.filter(Breed.breed == searched_breed).one()
        query = query.filter(Lost_Pet_Submission.breed_id == breed_id.breed_id)

#Not Working
    if searched_color:
        query = query.join(lostPetColor).join(Color) \
            .filter(Color.color == searched_color)



    # if searched_name_or_id:




    results = query.all()


    return jsonify({'data':render_template('petPoster_searchBar_temp.html', lost_pets = results)})


@app.route('/lost_poster_form', methods=['POST'])
def report_lost_pet_form(): 
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
    submitted_name = request.form.get('pet_name')
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
    date_lost = request.form.get('date_lost')
    user_email = session.get('logged_in_user_email')


    species = Species.query.filter(Species.species == submitted_species).one()
    for color in colors:
        queried_colors.append(Color.query.filter(Color.color == color).one())

    breed = Breed.query.filter(Breed.breed == submitted_breed,
                                 Breed.species_id == species.species_id).one()

    user = User.query.filter(User.email == user_email).one()

    lost_pet = Lost_Pet_Submission(species = species,
                                    breed = breed, 
                                    notes = submitted_notes, 
                                    photo = str(f.filename),
                                    latitude = submitted_latitude, 
                                    longitude = submitted_longitude, 
                                    pet_name = submitted_name,
                                    user_id = user.user_id, 
                                    date_lost = date_lost,
                                    colors = queried_colors
                                    )

    db.session.add(lost_pet)
    db.session.commit()
    print("submitted lost pet to database!")
    flash("Pet poster has been created!")
    return redirect('/lost_pet_posters')

@app.route('/report_a_pet_page')
def report_a_pet_page():
    """Allows user to report a lost pet."""

    colors = db.session.query(Color)
    breeds = db.session.query(Breed)

    if session.get("logged_in_user_email") == None:
        flash("Please sign in to report a lost pet")
        return render_template("login.html")

    else:
        return render_template("report_a_pet_page.html",
                                    colors=colors,
                                    breeds=breeds)




if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
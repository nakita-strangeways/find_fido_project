"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import Animal, Color, AnimalColor, Species, Breed, Size, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')


# @app.route("/users")
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("users.html", users=users)

# @app.route("/user_profile/<id>")
# def display_user_profile(id):
#     """ Displays a users AGE, ZIPCODE, and a list of movies/scores they've rated"""

#     selected_user = id  #selects user id from url
#     selected_user_data = User.query.get(selected_user)   # finds user in users table

#     all_users_movie_ratings = db.session.query(Rating.user_id, Rating.movie_id, Rating.score)  #gets all userid, movieid, rating from ratings table
#     selected_user_movies_ratings = all_users_movie_ratings.filter(Rating.user_id==selected_user)   #limits results to our selected user
    
#     # all_users_movies = db.session.query(Movie.title)  #gets all titles from movies table
#     # selected_user_movies = all_users_movies.filter(Rating.movie_id==selected_user)


#     return render_template("user_profile.html", selected_user_data=selected_user_data, 
#                         selected_user_movies_ratings=selected_user_movies_ratings)

#     #FINISH:
#     #Get movie title from movie table using movie id from ratings table and update html to reflect info



# @app.route("/register",methods = ["GET"])
# def display_register_form():
#     """ displays register form page """

#     return render_template("register_form.html")


# @app.route("/register",methods = ["POST"])
# def register_form():
#     """ registers new user """

#     user_email = request.form.get("email")
#     user_password = request.form.get("password")

#     session['s_user_email'] = user_email
#     session['s_user_password'] = user_password

#     sql = "SELECT email FROM users WHERE email = :email"

#     cursor = db.session.execute(sql, {'email': user_email})

#     user_result = cursor.fetchone()

#     if user_result == None:
#         sql = """INSERT INTO users (email, password) 
#                 VALUES (:email, :password) 
#                 """
#         db.session.execute(sql, {'email': user_email, 'password': user_password})

#     db.session.commit()

#     print(user_result)

#     return redirect("/")

# @app.route("/login",methods = ["GET"])
# def display_login_form():
#     """ displays the login page """

#     if session:
#         return redirect("/")

#     return render_template("login.html")

# @app.route("/login",methods = ["POST"])
# def login_form():
#     """ log in user """

#     user_email = request.form.get("email")
#     user_password = request.form.get("password")

#     session['s_user_email'] = user_email
#     session['s_user_password'] = user_password

#     sql = "SELECT user_id, email, password FROM users WHERE email = :email"

#     cursor = db.session.execute(sql, {'email': user_email, 'password': user_password})

#     user_result = cursor.fetchone()

#     # print(user_result[1], user_result[0])

#     if user_result == None:
#         flash('Wrong username. Please try again.')
#         return redirect('/login')

#     elif user_result[2] == user_password:
#         session['s_user_result'] = user_result[0]
#         flash('Login successful!')
#         return redirect('/')

#     else:
#         flash('Wrong password. Please try again.')
#         return redirect('/login')


# @app.route('/logout')
# def logout():
#     """Log out page."""
#     return render_template('logout.html')

# @app.route("/logout", methods = ["POST"])
# def logout_form():
#     """ Logs users out if they select the logout button """
#     logout = request.form.get("logOut")
#     stayLogIn = request.form.get("dontLogOut")
 
#     if logout:
#         session.clear()
#         flash('Logged Out')

#     if stayLogIn:
#         flash('Still Logged In')
#         #check this flash



#     return redirect("/")

    


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
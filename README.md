<img src="https://github.com/nakita-strangeways/find_fido_project/blob/master/static/icons/Logo_2.png" alt="FindFido_logo" title="FindFido" align="right" height="200" />

# FIND FIDO
A website that allows a community to come together to find their lost pets. 

### Tech Stack
* Python 
* JavaScript (AJAX, JSON)
* HTML
* CSS
* SQL

### Built With

* [Google Maps API](https://developers.google.com/maps/documentation/) - API 

## A Note From The Author
I originally studied the more technical side of animation for four years at the Academy of Art University. It's here that I got my first taste of python, which drove me to enroll at Hackbright Academy.

Around that time, my little sister lost her cat, Raven. The biggest problem was there was no way to tell if anyone in the community had seen Raven as well as pinpoint where or how far she had gone. Putting up posters wasn’t enough.

I created this project to help solve that problem, and to more directly involve the community in returning pets home.

## Lets Walk Through This!

<img src="https://github.com/nakita-strangeways/find_fido_project/blob/master/static/icons/homepage.png" alt="FindFido_homepage" title="FindFido_Homepage" height="500" />

<img src="https://github.com/nakita-strangeways/find_fido_project/blob/master/static/icons/cat-pin.png" alt="FindFido_CatPin" title="CatPin" height="70" align="right" />
<img src="https://github.com/nakita-strangeways/find_fido_project/blob/master/static/icons/dog-pin.png" alt="FindFido_DogPin" title="DogPin" height="70" align="right" />
<img src="https://github.com/nakita-strangeways/find_fido_project/blob/master/static/icons/found_pin.png" alt="FindFido_FoundPin" title="FoundPin" height="70" align="right" />

Find Fido is a web app that utilizes the community, photos, and google maps to create a network of stray or lost animals. The markers on the map reflect the animal species, as well as if it has been successfully found and returned home.


If a user has lost a pet, all they need to do is check the pets last seen location, either using their current location (if allowed), the address bar, or dragging the map. Once there, they can filter the map to fit their pets description. 

<img src="https://github.com/nakita-strangeways/find_fido_project/blob/master/static/icons/map_window.png" alt="map_window" title="map_window" height="250" align="left"/><img src="https://github.com/nakita-strangeways/find_fido_project/blob/master/static/icons/modal.png" alt="modal1" title="modal1" width="700" /><br>



Clicking one of the map pins opens a small window for quick glance searches. It contains a small image, the size, colors, and date/time seen. This way, a user looking for a lost pet can quickly check if it might be theirs. Because this is so small, users can click the window and open a modal with a larger image, and more information. 

The Modal has the same information as the window, and then some more, like notes about the sighting, and the username of the person who saw the animal/took the photo. Theres also a button that, if this is the users dog, and he is reunited with his family, can be clicked, and it will change the map pin to the green checkmark. 


<img src="https://github.com/nakita-strangeways/find_fido_project/blob/master/static/icons/missing_pets_page.png" alt="missing_pets_poster" title="missing posters" height="500" />

Lastly, there is a page where owners can submit their missing pets, like a missing pet poster. This lets the community know to what pets to keep an eye out for. Each "poster" has the pets name, an image of the pet, and the last date it was seen. Users can filter through the results to find particular pets, or pets in their neighborhood. When you click on a "poster," it opens a modal with more information, and a map of where it was lost at. 

<img src="https://github.com/nakita-strangeways/find_fido_project/blob/master/static/icons/modal2.png" alt="modal2" title="modal2" height="250" align="left"/>

Owners can report a missing pet poster by clicking the "Report Here!" button, which will direct them to a form. Once completed, the form will automatically redirect them to the missing posters page with their pet poster now created.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing purposes.

### Prerequisites

All prerequisites are in the requirements.txt file

```
Gblinker==1.4
click==6.7
Flask==1.0.2
Flask-DebugToolbar==0.10.1
Flask-SQLAlchemy==2.3.2
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
psycopg2==2.7.5
SQLAlchemy==1.2.8
Werkzeug==0.14.1
```

### Installing

Create a virtual environment and install requirements, using the `requirements.txt` file
```
$ virtualenv env
 New python executable in env/bin/python
 Installing setuptools, pip...done.
$ source env/bin/activate
(env) $ pip3 install -r requirements.txt
 Downloading/unpacking ...
 Successfully installed Flask Flask-SQLAlchemy Jinja2 ...
 Cleaning up...
```

Source the secrets from the `secrets.sh` file
```
(env) $ source secrets.sh
```

For the app to run, you will need to feed in the seed data, and set up PSQL tables:
```
(env) $ createdb (table name)
(env) $ python3 -i seed.py
```

This will start interactive python, where the following will print:
```
Colors inserted
Species inserted
Sizes inserted
Breeds inserted
Users inserted
Animals inserted
Animal Colors inserted
lost pets inserted
lostPet Colors inserted
```

Exit interactive python(`ctrl+c`). To open the app in your browser, run `server.py`

```
$ python3 server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

## Author

* **Nakita Strangeways** - *Initial work* - [Github](https://github.com/nakita-strangeways) [LinkedIn](https://www.linkedin.com/in/nakita-strangeways/)

## Acknowledgments

* Hackbright Instructors: [Dave Galbraith](https://github.com/davidvgalbraith), [Karin Hawley](https://github.com/khawley), and [Allian Roman](https://github.com/allianRoman)

* Mentors: [Dana Fallon](https://github.com/danafallon) and [Jeuel Wilkerson](https://github.com/JeuelyFish)

* Icon Designer/Artist: [Gus Gutierrez](https://www.instagram.com/gogogoose/?hl=en)

I couldn't have done it without you!

***


In memory of Raven <br> <br>
<img src="https://github.com/nakita-strangeways/find_fido_project/blob/master/static/icons/raven.png" alt="Raven" title="Raven" height="300"/> 
</center>


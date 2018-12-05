<img src="https://github.com/nakita-strangeways/find_fido_project/blob/master/static/icons/Logo_2.png" alt="Aimeos logo" title="Aimeos" align="right" height="60" />

# FIND FIDO
A website that allows a community to come together to find their lost pets. If a person sees a stray animal, they can take a photo and  submit a form of the animals description. 

## Tech Stack
* Python 
* JavaScript (AJAX, JSON)
* HTML
* CSS
* SQL

## Built With

* [Google Maps API](https://developers.google.com/maps/documentation/) - API 

## A note from the author
I originally studied the more technical side of animation for four years at the Academy of Art University. It's here that I got my first taste of python, which drove me to enroll at Hackbright Academy.

Around that time, my little sister lost her cat, Raven. The biggest problem was there was no way to tell if anyone in the community had seen Raven as well as pinpoint where or how far she had gone. Putting up posters wasn’t enough.

I created this project to help solve that problem, and to more directly involve the community in returning pets home.

***
***

## Lets walk through this!

COMING SOON

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

* **Nakita Strangeways** - *Initial work* - [Github](https://github.com/nakita-strangeways)

## Acknowledgments

* Hackbright Instructors: [Dave Galbraith](https://github.com/davidvgalbraith), [Karin Hawley](https://github.com/khawley), and [Allian Roman](https://github.com/allianRoman)

* Mentors: [Dana Fallon](https://github.com/danafallon) and [Jeuel Wilkerson](https://github.com/JeuelyFish)

***

In memory of Raven
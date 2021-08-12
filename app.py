import os

import requests
import random

from flask import Flask, flash, render_template, request, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm
from models import db, connect_db, User, Favorite, Quote, Character

CURR_USER_KEY = "curr_user"

API_URL = "https://the-one-api.dev/v2"
BEARER = "Bearer " + os.environ.get('ACCESS_TOKEN', "I_RmnBvwf8Ucp87KVImD ")
AUTH = {"Authorization" : BEARER}

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgres:///lotrdb').replace("://", "ql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "fyt87b98np")
toolbar = DebugToolbarExtension(app)

connect_db(app)

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("Successfully Logged Out!!", 'success')

    return redirect("/")


@app.route('/')
def home():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """
    
    if g.user:
        return render_template('home.html', user = g.user)
    else:
        return render_template('home-anon.html')


##############################################################################
# General user routes:

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    favorite_quotes_ids = (Favorite
                        .query
                        .filter(Favorite.user_id == user_id)
                        .all())

    favorite_quotes = []
    favorite_characters = []
    for f in favorite_quotes_ids:
        q = Quote.query.get(f.quote_id)
        favorite_quotes.append(q)
        favorite_characters.append(Character.query.filter(Character.api_id == q.character_id).first())

    return render_template('users/show.html', user=user, favorite_quotes=favorite_quotes, favorite_characters=favorite_characters)

##############################################################################
# Favorite routes:

@app.route('/users/favorite/<int:quote_id>')
def users_favorite(quote_id):
    """Sets the quote of the given id to a favorite for the user"""

    db.session.add(Favorite(quote_id = quote_id, user_id = g.user.id))
    db.session.commit()

    return redirect(f'/users/{g.user.id}')
    
@app.route('/users/unfavorite/<int:quote_id>')
def users_unfavorite(quote_id):
    """Removes the quote of the given id as favorite for the user"""

    to_unfavorite = Favorite.query.filter(Favorite.quote_id == quote_id).filter(Favorite.user_id == g.user.id).delete()
    db.session.commit()
    return redirect(f'/users/{g.user.id}')

##############################################################################
# Quotes routes:

@app.route('/quotes/random-quote')
def random_quote():
    """Returns a random quote"""

    if not is_initialized():
        init_characters_quotes()

    all_quotes = Quote.query.all()

    rand = random.randrange(0, len(all_quotes))
    rand_quote = all_quotes[rand]

    character = Character.query.filter(Character.api_id == rand_quote.character_id).first()

    return render_template("quotes/random-quote.html", quote = rand_quote, character = character)

@app.route('/quotes/search-quote')
def search_quote():
    """Search quotes by character"""

    if not is_initialized():
        init_characters_quotes()

    all_characters = Character.get_characters_with_quotes()

    search_words = request.args.get("q")
    character = request.args.get("character-names")

    results = []
    character_results = []

    if not search_words:
        search_words = ""

        if character != "Any" and character:
            results = find_quotes(search_words, character)
    else:
        results = find_quotes(search_words, character)

    for result in results:
        character = Character.query.filter(Character.api_id == result.character_id).first()
        character_results.append(character)

    return render_template(
        "quotes/quotes-search.html", all_characters=all_characters, search_words=search_words, results=results, character_results=character_results
    )



##############################################################################
# Games routes:

@app.route('/games/guess-character')
def guess_character():
    """Character guessing game"""

    character_array = []

    if not is_initialized():
        init_characters_quotes()

    all_quotes = Quote.query.all()
    all_characters = Character.get_characters_with_quotes()
    score = request.args.get("score")

    if not score:
        score = 0

    if int(score) > g.user.high_score:
        g.user.high_score = score
        db.session.commit()

    rand = random.randrange(0, len(all_quotes))
    rand_quote = all_quotes[rand]
    correct_character = Character.query.filter(Character.api_id == rand_quote.character_id).first()
    character_array.append(correct_character)

    for i in range(0, 3):
        rand = random.randrange(0, len(all_characters))
        rand_character = all_characters[rand]

        while rand_character in character_array:
            rand = random.randrange(0, len(all_characters))
            rand_character = all_characters[rand]

        character_array.append(rand_character)

    random.shuffle(character_array)

    return render_template("games/guess-character.html", quote = rand_quote, correct_character = correct_character, character_choices = character_array, score = score)


##############################################################################
# initialize db:

def init_characters_quotes():
    """Create the db columns for characters and quotes from the api"""

    all_quotes = requests.get(API_URL + "/quote", headers = AUTH).json()
    all_characters = requests.get(API_URL + "/character", headers = AUTH).json()

    for character in all_characters["docs"]:
        db.session.add(Character(api_id = character["_id"], character_name = character["name"]))

    for quote in all_quotes["docs"]:
        db.session.add(Quote(api_id = quote["_id"], quote_text = quote["dialog"], character_id = quote["character"]))

    db.session.commit()

    set_num_quotes()

    
def set_num_quotes():
    """Set the num_quotes property of each character in the database"""

    all_quotes = Quote.query.all()
    all_characters = Character.query.all()

    for character in all_characters:
        for quote in all_quotes:
            if character.api_id == quote.character_id:
                character.num_quotes = character.num_quotes + 1

                if character.character_name == "MINOR_CHARACTER":
                    character.character_name = "Unnamed character"

    db.session.commit()

def is_initialized():
    """Check if the database has been initialized with data from the api"""

    if len(Quote.query.all()) < 2:
        return False
    else:
        return True


##############################################################################
# search function:

def find_quotes(search_words, character_name):
    """Receives a string of search words and a name of a character to quote and returns all quotes that match"""

    results = []
    all_quotes = Quote.query.all()

    for quote in all_quotes:
        if character_name == "Any":
            if search_words.lower() in quote.quote_text.lower():
                results.append(quote)
        else:
            character = Character.query.filter(Character.character_name == character_name).first()

            if search_words == "":
                if character.api_id == quote.character_id:
                    results.append(quote)
            
            elif (search_words.lower() in quote.quote_text.lower()) and (character.api_id == quote.character_id):
                results.append(quote)

    return results



##############################################################################
# resume function:

@app.route('/resume')
def show_resume():
    return render_template("resume.html")
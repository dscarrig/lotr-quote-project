"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    high_score = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    favorites = db.relationship('Favorite')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def has_favorited(self, quote):
        has_fave = Favorite.query.filter(Favorite.user_id == self.id).filter(Favorite.quote_id == quote.id).all()

        if has_fave:
            return True
        else:
            return False

    @classmethod
    def signup(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method.
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Favorite(db.Model):
    """Connection of a user to a favorite quote"""

    __tablename__ = "favorites"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    quote_id = db.Column(
        db.Integer,
        db.ForeignKey('quotes.id', ondelete="cascade"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False
    )

class Quote(db.Model):
    """Quotes retrieved from the API."""

    __tablename__ = "quotes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    api_id = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    quote_text = db.Column(
        db.Text,
        nullable=False
    )

    character_id = db.Column(
        db.Text,
        db.ForeignKey('characters.api_id', ondelete="cascade")
    )

class Character(db.Model):
    """Characters retrieved from the API"""

    __tablename__ = "characters"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    api_id = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    character_name = db.Column(
        db.Text,
        nullable=False
    )

    num_quotes = db.Column(
        db.Integer,
        default=0
    )

    @classmethod
    def get_characters_with_quotes(self):
        result = []

        all_characters = Character.query.all()

        for character in all_characters:
            if character.num_quotes > 0 and character.character_name != "Test":
                result.append(character)

        return result


def connect_db(app):
    """Connect this database to provided Flask app.

    Called in Flask app.
    """

    db.app = app
    db.init_app(app)
"""Initialize database."""

from csv import DictReader
from app import db
from models import User, Quote, Character, Favorite

db.drop_all()
db.create_all()

User.signup(username = "Test", password = "Testpw")
db.session.add(Character(api_id = "abc", character_name = "Test"))
db.session.add(Quote(api_id = "123", quote_text = "heyy", character_id = "abc"))
db.session.add(Favorite(quote_id = 1, user_id = 1))

db.session.commit()
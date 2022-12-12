# lotr-quote-project

This site uses https://the-one-api.dev to create a database of all quotes and characters in The Lord of the Rings series of books. It has user account functionality where users can save quotes by favoriting them. The site has four main pages: a random quote generator, a character quote game, a list of user favorited quotes, and a page for searching for quotes by character or search terms.

The random quote page is the only page accessible without an account. It returns a random quote picked from any character. If the user is logged in they can favorite it.

The character quote game generates a random quote and four character choices to choose from. The user must pick the character who said the quote. A score counter keeps track of how many correct answers in a row the user guesses. Users' high scores are saved to their account.

When a user clicks their name on the top bar, they access a list of all quotes they have favorited. They can unfavorite these quotes on this page.

The quote search page allows the user to enter a string and search for any quotes containing that string. The user can also select a character from the drop down to narrow down the quotes. If the user selects a character and clicks search with an empty search form, they will be shown every quote said by that character. Users can favorite or unfavorite quotes here as well.

To run this site locally, postgresql must be installed. Then create a database in the lotr-quote-project directory called "lotrdb". This can be done with "createdb -h localhost -p 5432 -U postgres lotrdb", assuming you are using the default 5432 port and default postgres username. You may need to find a different open port and set the postgres user password before this can be created successfully.

Install all requirements for the app with "pip install -r requirements.txt". You may need to insall pip first. Then run seed.py to seed the database. Now launch the app with "flask run".

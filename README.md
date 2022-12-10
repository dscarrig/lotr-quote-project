# lotr-quote-project

This site uses https://the-one-api.dev to create a database of all quotes and characters in The Lord of the Rings series of books. It has user account functionality where users can save quotes by favoriting them. The site has four main pages: a random quote generator, a character quote game, a list of user favorited quotes, and a page for searching for quotes by character or search terms.

The random quote page is the only page accessible without an account. It returns a random quote picked from any character. If the user is logged in they can favorite it.

The character quote game generates a random quote and four character choices to choose from. The user must pick the character who said the quote. A score counter keeps track of how many correct answers in a row the user guesses. Users' high scores are saved to their account.

When a user clicks their name on the top bar, they access a list of all quotes they have favorited. They can unfavorite these quotes on this page.

The quote search page allows the user to enter a string and search for any quotes containing that string. The user can also select a character from the drop down to narrow down the quotes. If the user selects a character and clicks search with an empty search form, they will be shown every quote said by that character. Users can favorite or unfavorite quotes here as well.

To run this site locally, postgresql must be installed. Then a postgresql database called lotrdb must be created and seed.py must also be run before starting the application. The site is also hosted on https://lotr-quote-game.herokuapp.com/


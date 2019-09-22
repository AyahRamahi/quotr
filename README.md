# Quotr
Quotr is a web application built with Flask.

## What is Quotr ?
Quotr is a web application the I made using Flask microframework. Every time you open or refresh the index page you get a random quote from the database of quotes on the website , under it you will find the name of the person who said that quote and under it there is the username of the person who submitted this quote to our database. You can sign up an account and by logging in to your account you see the quotes you submitted and have a link that will direct you to submit quotes if you want .

## Screenshots
### Index Page
![](/screenshots/quotr.JPG)
### Login Page
![](/screenshots/quotr-login.JPG)
### Added Quotes Page
![](/screenshots/quotr-quotes.JPG)
### Add a Quote Page
![](/screenshots/quotr-add.JPG)

## Requirements
All requirements are in a file called **requirements.txt**, to download them all you can run this code in your terminal :
``` pip install -r requirements.txt ``` .

## Database
I have used Heroku free account to create a Postgresql database. To run this application you should provide a link to a database you have by putting the link in "DATABASE_URL" environment variable before running the program.


## License
[MIT](https://choosealicense.com/licenses/mit/)

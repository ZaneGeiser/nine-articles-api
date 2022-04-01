# Nine Articles Api
### An API for interacting with articles database. A Nine Junior Developer take home assignment

---

# QUICKSTART GUIDE FOR RUNNING THIS API

This app is written in python and utilises the Flask framwork. The articles data is stored in an SQLite database.
I have written and tested the app on **Python 3.9.10**. It should work on
python 3.8.x and later, however this is not tested. I have tested and
deployed on a Mac, but I believe this should work on PC or Linux.

### clone this repo to your machine
### set up Virtual Environment
In Terminal navigate to directory you have cloned the repo to.
open a virtual environment:
  Python's buit in vituval environment can be used like so:
  
  `python3 -m venv venv`
  
  creating a venv directory in your project.
  now activate the venv with:
  
  `source venv/bin/activate`
  
### install the dependancies.

`pip install -r requirements.txt`

### Set a few Flask variables
`export FLASK_APP=main.py`
`export FLASK_ENV=development`

### Start the server
`python3 main.py`

Now you should be able to navigete to [http://127.0.0.1:5000](http://127.0.0.1:5000) with an index page documenting the API Functionality.


# Testing the Functionality
I have tested this API using Postman to verify correct responses and updating of the database.


### files of note:
- **models.py** contains the Article object which holds the data for each article while it is being handeld in Python. It would have been simple to use only python dictionaries instead. However, the object allows some extra data validation and error handeling.
- **main.py** is the file that holds the three routes/endpoints. Flask handles that logic fairly elegently.
- **db_interface.py** is where I have written helper methods for reading and writing the data to the SQLite database.
- **start_articles.json** is a list of the 10 articles you should find on the database when you first start the app.
- **swagger.yaml** contains openapi documention for how this api should function. It is how I generated the API documentation located in templates/index.html


# Assumptions
- The API only provides these three endpoints.
### POST /articles
- When Posting an article to /articles the program accecpts json in the body of the request when **Content-Type is declared as application/json in the request header.**
- When POSTing, the json body should contain the keys correctly labeled. The app completes some checks to ensure the correct headers are present and that date values and tags values are in the correct format.
   - 'id'
   - 'title'
   - 'body'
   - 'date'
   - 'tags'
- I have assumed that when posting an article with an id that already exist, we want to update the existing data.
- currently if updating an article with new tags, the old tags are not removed from the database. This is an issue that needs to be fixed.

### GET /articles/{id}
- checks for the id in the database and returns a 404 error message if it is not
- return json with complete headers and values.
- the order of the article keys is scrambled. I believe is a property of the flask.jsonify() method. 
  
### GET /tags/{tagName}/{date}
- Checks that the date is in the correct format and then checks the database. If no matching tags are found It returns the same formated JSON but with empty data rather than an error.
  - Becasue the date does not include a timestamp, I could not return the last 10 articles with the correct ID as stipulated below. so I have elected to return a list with all articles. If however, simply returning any 10 articles from the day is wanted that could be easily implemented. If we want the last 10 submitted from that day, then we will have to update date to include time in the API documentaion, in the python handeling, and the SQLite server. 
  > The articles field contains a list of ids for the last 10 articles entered for that day.
- The order of the json keys is scrambled. I believe is a property of the flask.jsonify() method.

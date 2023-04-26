# News Aggregator

This is a web application that aggregates news from various sources and displays them on a single platform.

## Getting Started

### Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment: `python -m venv env`
4. Activate the virtual environment: `source env/bin/activate` (for Linux/MacOS) or `env\Scripts\activate` (for Windows)
5. Install the required packages: `pip install -r requirements.txt`
6. Migrate the database: `python manage.py migrate`
7. Create a superuser by running the following command : `python manage.py createsuperuser`.
8. Enter your username and password. After that you can create as many users as you would like by logging into the admin panel (http://127.0.0.1:8000/admin) in the user table through the superuser.
9. Create a .env file in your Django project's folder `(news_aggregator)` directory and add the following key/value pairs : 

REDDIT_API_URL="https://www.reddit.com/r/news/search.json"


NEWS_API_URL="https://newsapi.org/v2/everything"


NEWS_API_SECRET=  <Your API KEY>

  
You can get your API key by creating a free account on `https://newsapi.org/`

### Running the Application

1. Start the development server: `python manage.py runserver`
2. Refer to the `API Documentation.pdf` to get data from the APIs accordingly.

## Running Tests

To run the unit tests for this application, run the following command:

`python manage.py test`


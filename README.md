# promo-scraper

Web app to notify you the best deals for your specific interest.

## Running the app on your local computer

`git clone https://github.com/vitorrcunhaa/promo_scraper.git` or unpack compressed file(if you got this project via compressed file)

Go to `promo_scraper` dir

To run the Django app on your local computer, set up a Python development environment, including Python, pip, and virtualenv.

Create an isolated Python environment, and install dependencies:

LINUX/MACOS
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
WINDOWS
```
virtualenv env
env\scripts\activate
pip install -r requirements.txt
```

If you're on mac, you should have postgresql installed.

`brew install postgresql`

Run the Django migrations to set up your models:
```
python manage.py makemigrations
python manage.py migrate
```

Change Debug to True:

On promo_scraper/promo_scraper/settings.py
change line 27 to `DEBUG = True`


Start a local web server:

`python manage.py runserver`

In your browser, go to http://localhost:8000:


## Using the Django admin console

Create a superuser. You need to define a username and password.
`python manage.py createsuperuser`

Start a local web server:
`python manage.py runserver`

In your browser, go to http://localhost:8000/admin.

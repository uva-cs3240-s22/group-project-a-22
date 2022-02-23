# Group Project A22

## Development Setup
These are some instructions for setting up the development environment.

1. Clone the repository

2. Create and activate virtual environment.\
.venv is the environment name. This can be replaced with whatever you like.
```
python -m venv .venv

```
```
# for Windows
.venv/Scripts/activate.bat

# for Git Bash
source .venv/Scripts/activate
```


3. Install all the required packages
```
pip install -r requirements.txt
```

4. Setup local settings\
Copy the `local_settings.default.py` file in the `mysite` folder and rename it `local_settings.py`. This should automatically be removed from version control in the `.gitignore`. Then update the `local_settings.py` file with the Django secret key (this will be shared with you over a secure channel).

5. Make database migrations
```
python manage.py makemigrations
```
```
python manage.py migrate
```
6. Setup superuser account
```
python manage.py createsuperuser
```
You'll also want to setup a superuser on the postgres database. If you have already installed Heroku CLI, do that now.
```
heroku run python manage.py createsuperuser --app group-project-a22
```

Setup should now be complete. You can now host the repository locally with
```
python manage.py runserver
```
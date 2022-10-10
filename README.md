# EMBED PYTHON ASSESSMENT


## 1. Running the project with Docker

The first thing to do is to clone the repository using the git bash:

```bash
$ git clone https://github.com/myagmar-erdene/embed_assesment.git
```

Open the project's main folder in Windows Powershell:

```bash
$ cd embed_assessment
```

Run the following command to run Django's make migrations commands:
```bash
$ docker-compose run web python manage.py makemigrations social_network
$ docker-compose run web python manage.py migrate
```

Create a new superuser for your Django project, which will be useful to log in 
to project's admin page, where all the Models are registered and can be 
easily to manually add records to the tables:

```bash
$ docker-compuse run web python manage.py createsuperuser
```

Finally, use the following command to run the project using the docker-compose

```bash
$ docker-compose up
```

## 2. Running the project locally

The first thing to do is to clone the repository using the git bash:

```bash
$ git clone https://github.com/myagmar-erdene/embed_assesment.git
```

Open the project's main folder in Windows Powershell:

```bash
$ cd embed_assessment
```

Create a new Python virtual environment for the project:

```bash
$ python -m venv myvenv
```

where myvenv is the name of your new Python virtual environment

Activate the newly created virtual environment using the following command:

```bash
$ myvenvScripts/Activate.ps1
```

Upgrade pip and install the dependencies listed in requirements.txt:

```bash
(myvenv)$ pip install --upgrade pip
(myvenv)$ pip install -r requirements.txt
```

Please, note the (myvenv) in front of the prompt. This indicates that this 
terminal session operates in a virtual environment set up by myvenv.

Changing the Database configurations from PostgreSQL to SQLLite in project's
mysite/settings.py:

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Run the following command to run Django's make migrations commands:
```bash
(myvenv)$ python manage.py makemigrations social_network
(myvenv)$ python manage.py migrate
```

Create a new superuser for your Django project, which will be useful to log in 
to project's admin page, where all the Models are registered and can be 
easily to manually add records to the tables:

```bash
(myvenv)$ python manage.py createsuperuser
```

Finally, use the following command to run the project using the docker-compose

```bash
(myvenv)$ python manage.py runserver
```

## Notes
1. This project was developed on Windows 11, depending on your machine's OS
some terminal commands might not work as expected and might differ between
different OS.
2. It is also highly recommended to have downloaded and installed the following 
programming languages and tools on you local machine: 
* Python 3.10.7
* Docker Desktop 4.12.0
* Git bash 2.38.0

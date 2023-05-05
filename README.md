# Scientific Method App

**Author:** Lily Watt

**ReadMe Last Updated:** 04/05/2023

The goal of this project is to create an application that will help support the scientific method throughout the paper writing process. The app allows users to enter each step of the scientific method in a checklist format. Researchers mark those items as done and have reviewers then verify that each section of the report has been completed appropriately before the researchers move onto the next section. 

## Setup/Build/Install

To setup this project on your computer, clone the repositiory and inside scientific-method-app, run the following command to install the dependencies:
```bash
$ pip install -r requirements.txt
```
<br>

To build the development evironment, run:
```bash
$ docker compose -f docker-compose.yml up -d --build
```
To bring down the development containers and associated volumes, run:
```bash
$ docker compose -f docker-compose.yml down -v
```
<br>

To build the production environment, make sure you've filled out the ```.env.prod``` and ```.env.prod.db``` files first. Use the ```.env.prod.example``` and ```.env.prod.db.example``` files for templates and the ```.env.dev``` file for a reference. Once these files have been created, run:
```bash
$ docker compose -f docker-compose.prod.yml up -d --build
$ docker compose -f docker-compose.prod.yml exec -w /home/sm_app/web/sm_app web python manage.py migrate --noinput
$ docker compose -f docker-compose.prod.yml exec -w /home/sm_app/web/sm_app web python manage.py collectstatic --noinput
```
If you wish to make an admin user for the production environment, run the following command and enter the email, name and password you wish to use:
```bash
$ docker compose -f docker-compose.prod.yml exec -w /home/sm_app/web/sm_app web python manage.py createsuperuser
```
To bring down the production containers and associated volumes, run:
```bash
$ docker compose -f docker-compose.prod.yml down -v
```

## Usage

To use the program, if you're using the development environment, open ```http://localhost:8000/``` in a browser. If you're using the production environment, open ```http://localhost:1337/```. From there, freely use the application as you wish.

To access the admin page, open ```http://localhost:8000/admin/``` or ```http://localhost:1337/``` depending on your environment. If you're using the production environment, login with the details you used when you created the admin user. If you're using the development environment, an admin user has already been created. You can login with this account by using ```admin@superuser.com``` as the email and ```u0hN500N``` as the password. From here, you can view or select any database entry and add more or delete entries.

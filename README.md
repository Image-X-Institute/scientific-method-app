# Scientific Method App

**Author:** Lily Watt

**ReadMe Last Updated:** 12/06/2023

The goal of this project is to create an application that will help support the scientific method throughout the paper writing process. The app allows users to enter each step of the scientific method in a checklist format. Researchers mark those items as done and have reviewers then verify that each section of the report has been completed appropriately before the researchers move onto the next section. 

## Setup/Build/Install

To setup this project on your computer, first, follow the instructions to install Docker Desktop at https://docs.docker.com/get-docker/ and open it. 
Next, clone the repositiory and inside ```scientific-method-app```, run the following commands to build the development and production environments:
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

To build the production environment, setup the project on the computer you wish to act as the host. Additionally, make sure you've filled out the ```.env.prod``` and ```.env.prod.db``` files first. Use the ```.env.prod.example``` and ```.env.prod.db.example``` files for templates and the ```.env.dev``` file for a reference. Once these files have been created, run:
```bash
$ docker compose -f docker-compose.prod.yml up -d --build
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

To use the program, if you're using the development environment, open ```http://localhost:8000/``` in a browser on the host computer. If you're using the production environment, enter the IP Address of your host computer into a browser of a computer on the same network as the host computer. From there, freely use the web application as you wish.

To access the admin page, open the previous given link followed by ```.../admin/```. For example, ```http://localhost:8000/admin/``` or ```0.0.0.0/admin/```. If you're using the production environment, login with the details you used when you created the admin user. If you're using the development environment, an admin user has already been created. You can login with this account by using ```admin@superuser.com``` as the email and ```testing``` as the password. From here, you can view or select any database entry and add more or delete entries.

In the production environment, the web application will continue to be accessible as long as the Docker containers on the host computer remain on. Should the Docker containers be shut off at any point (i.e. due to the host computer shutting down or logging off), they can be simply reactivated by powering on the host computer and reopening Docker Desktop.

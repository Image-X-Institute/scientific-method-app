# Scientific Method App

**Author:** Lily Watt

**ReadMe Last Updated:** 24/02/2023

The goal of this project is to create an application that will help support the scientific method throughout the paper writing process. The app allows users to enter each step of the scientific method in a checklist format. Researchers mark those items as done and have reviewers then verify that each section of the report has been completed appropriately before the researchers move onto the next section. 

## Setup/Build/Install

To set-up the database functionality on your computer, clone the repositiory and inside scientific-method-app run:
```python
python3 manage.py makemigrations
```
Once you've done this, follow it up with:
```python
python3 manage.py migrate 
```
Once you've created the databases that will be used to store the data, you'll want to create an admin user. To do this, run:
```python
python3 manage.py createsuperuser
```
From there, enter the email and password that you want to use for the admin account.

## Usage

To use the program, simply run the following command inside the scientific-method-app folder:
```python
python3 manage.py runserver
```
This should give you a link to view the web application with at the line ```Starting development server at [link]```. For example, ```http://127.0.0.1:8000/```. Open that link and from there, login as any user accounts you've created or register a new one.

To add more database entries, head to the link listed in the terminal followed by ```.../admin/```. For example, ```http://127.0.0.1:8000/admin/```. Enter the details you used when you created the admin user and login. From here, you can select any database entry and add more or delete entries.

## Directory Structure

*To be written.*

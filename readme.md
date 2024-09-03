# Geo Test Project
This is the test project for AIInfraSolutions. 
It has some basic functionalities, such as a CRUD interface for a feature collection, and a map to display the features, as well as a page to edit the properties of the features.
It is written in Django and uses PostGIS for the database, some Bootstrap and OpenLayers for the frontend, as well as Docker for deployment.


![Janky cover picture](https://i.imgur.com/txX7asO.png)

## Disclaimer
This code is not hardend for production use, it is just a test project.
No proper user management is implemented, so the superuser is used for everything.
The Django server runs with debug mode, which is not recommended for production.
No Gunicorn or similar software is used, so the server is not production ready.

## Installation

### Using Docker
1. Clone the repository
```bash
git clone https://github.com/Valentinbist/mapTests.git
```
2. Change into the directory
```bash
cd mapTests
```
4. Change the settings in dev.env, if you want to (recommended for deployment, but deployment is not recommended :D)
5. Run the docker container
```bash
docker compose up
```
6. Make the migrations (they are not run in the entrypoint, since I don't like to run them each time, so you have to run them manually)
```bash
docker compose run web python manage.py makemigrations
docker compose run web python manage.py migrate
```
7. Make a superuser, since no proper user managaement is implemented
```bash
docker compose run web python manage.py createsuperuser
```
8. Load the default GeoJSON file (if you want to)
```bash
docker compose run web python manage.py load_geojson
```


### Local Installation
If you don't know how to set this project up locally, I recommend using the Docker container, since it is easier to set up.

Some insights:
Use Python 3.10 and look at the Dockerfile for the dependencies and the Docker install instructions.
As a tip: use ubuntu to more easily get PostGIS and GDAL running.



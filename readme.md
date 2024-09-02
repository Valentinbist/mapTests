# geoJSON test API

## Installation
2. make the migrations (they are not run in the entrypoint, since I don't like to run them each time, so you have to run the manually)
```bash
docker compose run web python manage.py makemigrations
docker compose run web python manage.py migrate
```
3. make a superuser, since no proper user managaement is implemented yet
```bash
docker compose run web python manage.py createsuperuser
```

#### Loading default dataset:
```bash
docker compose run web python manage.py load_geojson
```


## Todos
- [ ] Add more tests
- [ ] Add more documentation
- [ ] Find out if i need to get the features one level up in tje json so then the fitler and the pages might work
look in the copilot stuff and here https://medium.com/@dmitry.sobolevsky/feature-and-featurecollection-in-geojson-f36ec38ebdb1



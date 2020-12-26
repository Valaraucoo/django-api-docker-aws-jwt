### Django-API with heroku, docker and AWS S3

Run locally:
```bash
python manage.py runserver
```
or deploy on production:
```bash
heroku container:push web -a=wozniak-dev-api
heroku container:release web -a=wozniak-dev-api
```
You can find API documentation [here](https://wozniak-dev-api.herokuapp.com/docs/).
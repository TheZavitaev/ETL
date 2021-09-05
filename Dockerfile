FROM python:3.9.6-slim-bullseye

WORKDIR /code

COPY movies_admin/requirements/*.txt requirements/

RUN pip install -r requirements/production.txt

COPY ./movies_admin .

RUN python manage.py collectstatic --noinput

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
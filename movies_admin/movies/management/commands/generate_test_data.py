import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from tqdm import tqdm

from movies.factories import FilmWorkFactory, PersonFactory, GenreFactory
from movies.models import FilmWork, FilmWorkPerson, GenreFilmWork, Person, Genre, FilmWorkType, RoleType

PERSONS = 10000
FILMS = 100000
GENRES = 10

BATCH_SIZE = 50000
TEST = 10


class Command(BaseCommand):
    help = 'Создаем тестовые данные'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создаем данные...')

        self.stdout.write('Генерируем фильмы...')
        films = generate_films()

        self.stdout.write('Генерируем жанры...')
        genres = generate_genres()

        self.stdout.write('Генерируем персон...')
        persons = generate_persons()

        self.stdout.write('Создаем связи...')

        self.stdout.write('Генерируем жанры фильма и актеров...')
        genres_films_work = []
        films_work_persons = []

        for film in tqdm(films):
            genre_film_work = GenreFilmWork()
            genre_film_work.film_work = film
            genre_film_work.genre = random.choice(genres)
            genres_films_work.append(genre_film_work)

            for _ in range(random.randint(1, 20)):
                film_work_person = FilmWorkPerson()
                film_work_person.film_work = film
                film_work_person.person = random.choice(persons)
                film_work_person.role = random.choices(RoleType.choices)
                films_work_persons.append(film_work_person)

        self.stdout.write('Все данные сгенерированы')

        self.stdout.write('Сохраняем данные в БД...')

        self.stdout.write('Сохраняем персон...')
        Person.objects.bulk_create(tqdm(persons))

        self.stdout.write('Сохраняем жанры...')
        Genre.objects.bulk_create(tqdm(genres))

        self.stdout.write('Сохраняем фильмы...')
        FilmWork.objects.bulk_create(tqdm(films), batch_size=BATCH_SIZE)

        self.stdout.write('Сохраняем жанры конкретных фильмов в БД...')
        GenreFilmWork.objects.bulk_create(tqdm(genres_films_work), batch_size=BATCH_SIZE)

        self.stdout.write('Сохраняем персон фильмов в БД...')
        try:
            FilmWorkPerson.objects.bulk_create(tqdm(films_work_persons), batch_size=BATCH_SIZE)
        except IntegrityError:  # игнорируем ошибку с защитой от вставки повторяющихся данных
            pass

        self.stdout.write('Создание фейковых данных завершено!')


def generate_films():
    films = []
    for _ in tqdm(range(FILMS)):
        film = FilmWorkFactory.build(type=type)
        film.type = FilmWorkType.MOVIE
        films.append(film)
    return films


def generate_genres():
    genres = []
    for _ in tqdm(range(GENRES)):
        genre = GenreFactory.build()
        genres.append(genre)
    return genres


def generate_persons():
    persons = []
    for _ in tqdm(range(PERSONS)):
        person = PersonFactory.build()
        persons.append(person)
    return persons

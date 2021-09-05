import datetime
from random import randint

import factory
from factory import Faker, fuzzy
from factory.django import DjangoModelFactory
from pytz import UTC

from movies.models import FilmWork, MPAARatingType, FilmWorkType
from .models import Person, Genre


class GenreFactory(DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Faker('company')
    description = factory.Faker('sentence', nb_words=128, variable_nb_words=True)
    created_at = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))


class FilmWorkFactory(DjangoModelFactory):
    class Meta:
        model = FilmWork

    id = Faker('uuid4')
    title = Faker('company')
    description = Faker('sentence', nb_words=128, variable_nb_words=True)
    creation_date = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(2000, 1, 1, tzinfo=UTC))
    certificate = Faker('company')
    mpaa_rating = fuzzy.FuzzyChoice(MPAARatingType)
    rating = fuzzy.FuzzyDecimal(0, 9.9)
    type = fuzzy.FuzzyChoice(FilmWorkType)
    genres = factory.RelatedFactoryList(
        GenreFactory,
        size=randint(1, 4),
    )
    created_at = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))
    updated_at = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    full_name = factory.Faker('name')
    birth_date = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))
    created_at = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))

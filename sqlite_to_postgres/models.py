import uuid
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class FilmWork:
    title: str
    description: str
    rating: float
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    _table: ClassVar[str] = 'content.film_work'
    _uniq_field: ClassVar[str] = 'title'


@dataclass
class Genre:
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    _table: ClassVar[str] = 'content.genre'
    _uniq_field: ClassVar[str] = 'name'


@dataclass
class Person:
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    _table: ClassVar[str] = 'content.person'
    _uniq_field: ClassVar[str] = 'name'


@dataclass
class FilmWorkGenre:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    _table: ClassVar[str] = 'content.film_work_genre'


@dataclass
class FilmWorkPerson:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    _table: ClassVar[str] = 'content.film_work_person'
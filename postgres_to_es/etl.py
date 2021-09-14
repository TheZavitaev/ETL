import datetime
import os
from functools import wraps
from time import sleep

import psycopg2
from elasticsearch import Elasticsearch
from psycopg2.extras import DictCursor

from extractor import PostgresExtractor
from loader import ESLoader
from postgres_to_es.config import FILE_NAME, logger, dsl
from postgres_to_es.helpers import connect_to_database
from postgres_to_es.models import JsonFileStorage, State
from transformer import Transformer


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


def etl(target):
    json_file_storage = JsonFileStorage(FILE_NAME)
    state = State(json_file_storage)
    begin_date = state.get_state('pointer_begin_date') or datetime.datetime(year=2000, month=1, day=1)
    state.set_state('pointer_begin_date', str(begin_date))

    logger.info('Started ETL')
    while True:
        pointer_begin_date = datetime.datetime.strptime(state.get_state('pointer_begin_date'), '%Y-%m-%d %H:%M:%S')
        pointer_end_date = pointer_begin_date + datetime.timedelta(days=1)
        now = datetime.datetime.now()

        while now < pointer_end_date:
            logger.info(
                f'ETL {now=} < {pointer_end_date=}. Wait one hour')
            sleep(3600)

        target.send(['film_work', 'title', pointer_begin_date, pointer_end_date])
        target.send(['person', 'full_name', pointer_begin_date, pointer_end_date])
        target.send(['genre', 'name', pointer_begin_date, pointer_end_date])

        state.set_state('pointer_begin_date', str(pointer_end_date))
        sleep(0.1)


@coroutine
def extract(target, extractor: PostgresExtractor):
    """Retrieving non-indexed data."""

    while key := (yield):
        table, column, pointer_begin_date, pointer_end_date = key
        extractor.get_data(
            target=target,
            table=table,
            column=column,
            pointer_begin_date=pointer_begin_date,
            pointer_end_date=pointer_end_date
        )


@coroutine
def transform(target, transformer: Transformer):
    """Preparing records for uploading to ES."""

    while key := (yield):
        result, table, column = key
        transformed = []
        for row in result:
            transformed.append(transformer.transform(row, column))

        target.send([transformed, table, column])


@coroutine
def load(loader: ESLoader):
    """Load to ES."""

    while key := (yield):

        transformed, table, column = key
        if len(transformed) == 0:
            continue

        logger.debug(f'ETL. Loaded start {table}. {len(transformed)} items.')
        loader.load(transformed, table)
        logger.debug(f'ETL. Loaded stop {table}. {len(transformed)} items.')


if __name__ == '__main__':

    while not connect_to_database():
        logger.info(f'ETL. Wait connect to database Postgres. 10 sec.')
        sleep(10)

    es = Elasticsearch([os.getenv('ES_HOST', 'http://localhost:9200/')])

    while not es.ping():
        logger.info(f'ETL. Wait connect to database Elasticsearch. 10 sec.')
        sleep(10)

    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        loader = load(ESLoader(os.getenv('ES_HOST', 'http://localhost:9200/')))
        transformer = transform(loader, Transformer())
        extractor = extract(transformer, PostgresExtractor(pg_conn))
        etl(extractor)

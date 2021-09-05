import psycopg2
from psycopg2.extras import DictCursor

from postgres_to_es.config import logger, dsl


def connect_to_database():
    """Function to connect to Postgres."""

    conn = None
    try:
        conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logger.info(f'ETL. Connect to Postgres ERROR. {error}')
    return False

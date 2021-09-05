import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from config import dsl

# у меня относительные импорты в данной сборке работать отказываются
try:
    from .utils.sqlite_loader import SQLiteLoader
    from .utils.postgres_saver import PostgresSaver
except ImportError:
    from utils.sqlite_loader import SQLiteLoader
    from utils.postgres_saver import PostgresSaver


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

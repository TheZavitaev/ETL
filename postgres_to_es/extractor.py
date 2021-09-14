from psycopg2.extensions import connection as _connection
from psycopg2.extras import RealDictCursor

from postgres_to_es.config import PAGE, logger


class PostgresExtractor:
    data = []

    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = pg_conn.cursor(cursor_factory=RealDictCursor)

    def get_data(self, target, table, column, pointer_begin_date, pointer_end_date):
        """
        Receives non-indexed movies

        :return: result
        """
        sql = f"""
            SELECT
                id,
                {column} 
            FROM content."content.{table}" d 
            WHERE d.modified <= to_date( '{str(pointer_end_date)}', 'YYYY-MM-DD HH24:MI:SS' ) 
            AND d.modified > to_date( '{str(pointer_begin_date)}', 'YYYY-MM-DD HH24:MI:SS' )
        """

        self.cursor.execute(sql)
        
        while True:
            rows = self.cursor.fetchmany(PAGE)

            if not rows:
                break

            logger.info(
                f'EXTRACTOR. Extract start {table}. {pointer_begin_date=}, {pointer_end_date=}. {len(rows)} items.')

            target.send([rows, table, column])

            logger.info(
                f'EXTRACTOR. Extract stop {table}. {pointer_begin_date=}, {pointer_end_date=}. {len(rows)} items.')

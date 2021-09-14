import logging
import os

from dotenv import load_dotenv

load_dotenv()

# Logging settings
logging.basicConfig(filename='etl.log', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Postgres settings
PAGE = 50
dsl = {
    'dbname': os.getenv('dbname', 'postgres'),
    'user': os.getenv('user', 'postgres'),
    'password': os.getenv('password', 'postgres'),
    'host': os.getenv('host', 'localhost'),
    'port': os.getenv('port', 5432),
    'options': '-c search_path=content,postgres',
}

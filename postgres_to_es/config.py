import logging
import os

from dotenv import load_dotenv

load_dotenv()

# Logging settings
logging.basicConfig(filename='etl.log', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Storage settings
FILE_NAME = 'storage.json'

# Postgres settings
PAGE = 50
dsl = {
    'dbname': os.getenv('dbname'),
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'port': os.getenv('port')
}

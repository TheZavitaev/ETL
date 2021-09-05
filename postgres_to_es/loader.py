import json
from urllib.parse import urljoin

import requests

from postgres_to_es.config import logger


class ESLoader:
    def __init__(self, url: str):
        self.url = url

    def load(self, data, table):
        self.load_to_es(data, table)

    def _get_es_bulk_query(self, rows: list[dict], index_name: str) -> list[str]:
        """Prepares bulk request in Elasticsearch."""

        prepared_query = []

        for row in rows:
            prepared_query.extend(
                [
                    json.dumps(
                        {
                            'index': {
                                '_index': index_name,
                                '_id': row.get('id')
                            }
                        }
                    ),
                    json.dumps(row)
                ]
            )

        return prepared_query

    def load_to_es(self, records: list[dict], index_name: str):
        """Sending a request to ES and parsing data saving errors."""

        prepared_query = self._get_es_bulk_query(records, index_name)
        str_query = '\n'.join(prepared_query) + '\n'

        response = requests.post(
            urljoin(self.url, '_bulk'),
            data=str_query,
            headers={'Content-Type': 'application/x-ndjson'}
        )

        json_response = json.loads(response.content.decode())

        for item in json_response.get('items'):
            if error_message := item.get('error'):
                logger.error(error_message)

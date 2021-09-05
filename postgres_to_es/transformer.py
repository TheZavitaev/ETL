class Transformer:

    def transform(self, row, column) -> dict:
        """
        Converting field names to structure for elastic search

        :param row: row to convert
        :param column: column
        :return: ES structure
        """

        return {
                'id': row.get('id'),
                column: row.get(column)
            }

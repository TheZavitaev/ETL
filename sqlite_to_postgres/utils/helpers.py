from datetime import datetime


def create_tuple(row):
    line = tuple()

    for value in row.values():
        if value is None:
            value = ''
        if type(value) == datetime:
            value = value.strftime('%Y-%m-%d')
        if type(value) == float:
            value = str(value)

        line = (*line, str(value))
    return line

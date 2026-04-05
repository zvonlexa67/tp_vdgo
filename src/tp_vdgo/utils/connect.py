import sys
import psycopg
from contextlib import contextmanager, suppress

class Rollback(Exception):
    ...

def rollback():
    raise Rollback()

@contextmanager
def connect(conn_text = "", cls = None):
    if cls:
        rf = psycopg.rows.class_row(cls)
    else:
        rf = psycopg.rows.dict_row

    connection = psycopg.connect(conn_text)

    with suppress(Rollback):
        try:
            yield connection.cursor(row_factory=rf)
        finally:
            exc_type, exc_value, traceback = sys.exc_info()
            if exc_value:
                connection.rollback()
            else:
                connection.commit()
            connection.close()


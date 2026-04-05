from .db import db, testdb

def dropdb():
    if testdb("template1"):
        dbP = db()
        dbP.dbname = "template1"
        with dbP.cursor(autocommit=True) as cur:
            cur.execute(f"DROP DATABASE {dbP.settings.db_name};")
from .db import db, testdb

def dropusers():
    if testdb("template1"):
        dbP = db()
        dbP.dbname = "template1"
        settings = dbP.settings
        with dbP.cursor() as cur:
            for u in settings.users:
                cur.execute(f"DROP USER IF EXISTS {u.puser};")
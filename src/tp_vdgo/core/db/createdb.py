from .db import db, testdb

def createdb():
    if not testdb(exp=False) and testdb("template1"):
        dbP = db()
        settings = dbP.settings
        dbP.dbname = "template1"
        dbP.user = settings.super_vdgo.puser
        dbP.passwd = settings.super_vdgo.passwd

        with dbP.cursor(autocommit=True) as cur:
            cur.execute(f"CREATE DATABASE {settings.db_name};")
from .db import db, testdb

def createusers():
    if testdb("template1"):
        dbP = db()
        dbP.dbname = "template1"
        settings = dbP.settings
    
        with dbP.cursor() as cur:
            for u in settings.users:
                match u.puser:
                    case "super_vdgo":
                        cur.execute(f"""
                            CREATE ROLE {u.puser} WITH
                                LOGIN
                                NOSUPERUSER
                                INHERIT
                                CREATEDB
                                NOCREATEROLE
                                NOREPLICATION
                                NOBYPASSRLS
                                PASSWORD '{u.passwd}';
                        """)
                    case _:
                        cur.execute(f"""
                            CREATE ROLE {u.puser} WITH
                                LOGIN
                                NOSUPERUSER
                                INHERIT
                                NOCREATEDB
                                NOCREATEROLE
                                NOREPLICATION
                                NOBYPASSRLS
                                PASSWORD '{u.passwd}';
                        """)
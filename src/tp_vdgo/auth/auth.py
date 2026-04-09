from ..db import db
from ..models import Role, User


class BaseAuth():
    def __init__(self):
        self._db_super_vdgo = db_super_vdgo = db()
        self._settings = settings = db_super_vdgo.settings
        self._db_super_vdgo.user = settings.super_vdgo.puser
        self._db_super_vdgo.passwd = settings.super_vdgo.passwd

class Auth(BaseAuth):
    def __init__(self):
        super().__init__()

    def drop(self):
        with self._db_super_vdgo.cursor() as cur:
            cur.execute(User.get_pg_pg_table_drop())
            cur.execute(Role.get_pg_table_drop())

    def create(self):
        with self._db_super_vdgo.cursor() as cur:
            cur.execute(Role.get_pg_table_definition())
            cur.execute(User.get_pg_table_definition())

    
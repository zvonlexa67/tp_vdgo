import sys
import psycopg
from contextlib import contextmanager, suppress

from ..config import Settings

class _cursor_wrapper():
    """Пробрасывает execute-вызовы, сохраняя последний запрос в db-объекте."""
    def __init__(self, cursor, db_instance):
        self.__cursor = cursor
        self.__db = db_instance

    def execute(self, query, params=None, **kwargs):
        self.__db.last_query = query
        if params is not None:
            return self.__cursor.execute(query, params, **kwargs)
        return self.__cursor.execute(query, **kwargs)

    def executemany(self, query, params_list, **kwargs):
        self.__db.last_query = query
        return self.__cursor.executemany(query, params_list, **kwargs)

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        return getattr(self.__cursor, name)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass  # контекстный менеджер управляется внешним db.cursor()

class db():
    def __init__(self, conn_params = None):
        self.__settings = settings = Settings()

        if conn_params:
            self.__conn_params = conn_params
        else:
            self.__db_host = settings.db_host
            self.__db_port = settings.db_port
            self.__db_name = settings.db_name
            self.__db_user = settings.db_user
            self.__db_pass = settings.db_pass

            self.conn_params()

    def conn_params(self):
        self.__conn_params = f"""
            host={self.__db_host} 
            port={self.__db_port}
            dbname={self.__db_name} 
            user={self.__db_user} 
            password={self.__db_pass} 
        """

    class Rollback(Exception):
        ...

    @contextmanager
    def cursor(self, cls = None, autocommit = False):
        if cls:
            row_factory = psycopg.rows.class_row(cls)
        else:
            row_factory = psycopg.rows.dict_row

        try:
            self.__connection = psycopg.connect(self.__conn_params, autocommit=autocommit)
        except psycopg.OperationalError as e:
            raise RuntimeError(f"Не удалось подключиться к базе данных: {e}") from e

        self.__last_query = None

        with suppress(self.Rollback):
            try:
                cur = self.__connection.cursor(row_factory=row_factory)
                yield _cursor_wrapper(cur, self)
            finally:
                exc_type, exc_value, traceback = sys.exc_info()
                if exc_value:
                    self.__connection.rollback()

                    raise RuntimeError(f"Не удалось выполнить SQL запрос: {self.__last_query}\n {exc_value}")
                else:
                    if not autocommit:
                        self.__connection.commit()
                self.__connection.close()

    @property
    def host(self):
        return self.__db_host
    
    @host.setter
    def host(self, value):
        self.__db_host = value
        self.conn_params()

    @property
    def port(self):
        return self.__db_port
    
    @port.setter
    def port(self, value):
        self.__db_port = value
        self.conn_params()

    @property
    def dbname(self):
        return self.__db_name
    
    @dbname.setter
    def dbname(self, value):
        self.__db_name = value
        self.conn_params()

    @property
    def user(self):
        return self.__db_user
    
    @user.setter
    def user(self, value):
        self.__db_user = value
        self.conn_params()

    @property
    def passwd(self):
        return self.__db_pass
    
    @passwd.setter
    def passwd(self, value):
        self.__db_pass = value
        self.conn_params()

    @property
    def get_db_name(self):
        return self.db_tp_vdgo
    
    @property
    def params(self):
        return self.__conn_params

    @property
    def info(self):
        return self.__connection.info

    @property
    def settings(self):
        return self.__settings

    @property
    def last_query(self):
        return self.__last_query

    @last_query.setter
    def last_query(self, value):
        self.__last_query = value
    
def conn_parms(host, port, dbname, user, password):
    return f"""
        host={host} 
        dbname={dbname} 
        user={user} 
        password={password} 
        port={port}
    """

# def createusers():
#     if testdb("template1"):
#         dbP = db()
#         dbP.dbname = "template1"
#         settings = dbP.settings
    
#         with dbP.cursor() as cur:
#             for u in settings.users:
#                 match u.puser:
#                     case "super_vdgo":
#                         cur.execute(f"""
#                             CREATE ROLE {u.puser} WITH
#                                 LOGIN
#                                 NOSUPERUSER
#                                 INHERIT
#                                 CREATEDB
#                                 NOCREATEROLE
#                                 NOREPLICATION
#                                 NOBYPASSRLS
#                                 PASSWORD '{u.passwd}';
#                         """)
#                     case _:
#                         cur.execute(f"""
#                             CREATE ROLE {u.puser} WITH
#                                 LOGIN
#                                 NOSUPERUSER
#                                 INHERIT
#                                 NOCREATEDB
#                                 NOCREATEROLE
#                                 NOREPLICATION
#                                 NOBYPASSRLS
#                                 PASSWORD '{u.passwd}';
#                         """)

# def dropusers():
#     if testdb("template1"):
#         dbP = db()
#         dbP.dbname = "template1"
#         settings = dbP.settings
#         with dbP.cursor() as cur:
#             for u in settings.users:
#                 cur.execute(f"DROP USER IF EXISTS {u.puser};")

# def createdb():
#     if not testdb(exp=False) and testdb("template1"):
#         dbP = db()
#         settings = dbP.settings
#         dbP.dbname = "template1"
#         dbP.user = settings.super_vdgo.puser
#         dbP.passwd = settings.super_vdgo.passwd

#         with dbP.cursor(autocommit=True) as cur:
#             cur.execute(f"CREATE DATABASE {settings.db_name};")

# def dropdb():
#     if testdb("template1"):
#         dbP = db()
#         dbP.dbname = "template1"
#         with dbP.cursor(autocommit=True) as cur:
#             cur.execute(f"DROP DATABASE {dbP.settings.db_name};")

def testdb(dbname=None, exp=True):
    if dbname:
        dbP = db()
        dbP.dbname = dbname
    else:
        dbP = db()

    status = 0
    try:
        with dbP.cursor() as cur:
            cur.execute("SELECT 1;")
        status = dbP.info.status
    except RuntimeError as e:
        if exp:
            raise RuntimeError(e)

    return status

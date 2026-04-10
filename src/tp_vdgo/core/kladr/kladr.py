from dbfread2 import DBF
import asyncio
import asyncpg
from typing import Dict, List

from ..db import db
from ...config import Settings
from ...models import Kladr, Altnames, Doma, SocrBase, Street, Flat, NameMap

class base_kladr():
    def __init__(self):
        self._settings = settings = Settings()

        self._conn_params = f"postgresql://{settings.super_vdgo.puser}:{settings.super_vdgo.passwd}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

class utils_kladr(base_kladr):
    def __init__(self):
        super().__init__()
        self._dbT = db()
        self._dbT.user = self._settings.super_vdgo.puser
        self._dbT.passwd = self._settings.super_vdgo.passwd

    def truncate(self):
        with self._dbT.cursor() as cur:
            cur.execute(f"TRUNCATE TABLE {self._settings.altnames.table};")
            cur.execute(f"TRUNCATE TABLE {self._settings.doma.table};")
            cur.execute(f"TRUNCATE TABLE {self._settings.flat.table};")
            cur.execute(f"TRUNCATE TABLE {self._settings.kladr.table};")
            cur.execute(f"TRUNCATE TABLE {self._settings.namemap.table};")
            cur.execute(f"TRUNCATE TABLE {self._settings.socrbase.table};")
            cur.execute(f"TRUNCATE TABLE {self._settings.street.table};")

    def drop(self):
        with self._dbT.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {self._settings.altnames.table};")
            cur.execute(f"DROP TABLE IF EXISTS {self._settings.doma.table};")
            cur.execute(f"DROP TABLE IF EXISTS {self._settings.flat.table};")
            cur.execute(f"DROP TABLE IF EXISTS {self._settings.kladr.table};")
            cur.execute(f"DROP TABLE IF EXISTS {self._settings.namemap.table};")
            cur.execute(f"DROP TABLE IF EXISTS {self._settings.socrbase.table};")
            cur.execute(f"DROP TABLE IF EXISTS {self._settings.street.table};")

    def create(self):
        with self._dbT.cursor() as cur:
            cur.execute(Altnames.get_pg_table_definition())
            print(f"CREATED TABLE {self._settings.altnames.table}")

            cur.execute(Doma.get_pg_table_definition())
            print(f"CREATE TABLE {self._settings.doma.table}")
            
            cur.execute(Kladr.get_pg_table_definition())
            print(f"CREATE TABLE {self._settings.kladr.table}")

            cur.execute(Street.get_pg_table_definition())
            print(f"CREATE TABLE {self._settings.street.table}")

            cur.execute(SocrBase.get_pg_table_definition())
            print(f"CREATE TABLE {self._settings.socrbase.table}")

            cur.execute(Flat.get_pg_table_definition())
            print(f"CREATE TABLE {self._settings.flat.table}")

            cur.execute(NameMap.get_pg_table_definition())
            print(f"CREATE TABLE {self._settings.namemap.table}")

class kladr(base_kladr):
    def __init__(self):
        super().__init__()
        self._conn_params = f"postgresql://{self._settings.super_vdgo.puser}:{self._settings.super_vdgo.passwd}@{self._settings.db_host}:{self._settings.db_port}/{self._settings.db_name}"
    
    async def loadDBF(self):
        ch = check_kladr_dbf()
        if ch.check_file():
            print("Все файлы DBF обнаружены")

            await self.run(self._settings.altnames.path, self._settings.altnames.table)
            await self.run(self._settings.doma.path, self._settings.doma.table)
            await self.run(self._settings.kladr.path, self._settings.kladr.table)
            await self.run(self._settings.street.path, self._settings.street.table)
            await self.run(self._settings.socrbase.path, self._settings.socrbase.table)
            await self.run(self._settings.flat.path, self._settings.flat.table)
            await self.run(self._settings.namemap.path, self._settings.namemap.table)

    async def run(self, file=None, table=None):
        if file and table:
            print(f"Загрузка файла - {file}")
            queue = asyncio.Queue(maxsize=5)

            adl = stream_dbf_loader(file=file, table=table, queue=queue, conn_params=self._conn_params)
            producer_task = asyncio.create_task(adl.producer())
            consumer_task = asyncio.create_task(adl.consumer())
        
            await asyncio.gather(producer_task, consumer_task)
            print(f"Выгрузка в таблицу - {table}")

class check_kladr_dbf(base_kladr):
    def __init__(self):
        super().__init__()
        self.__encoding = "cp866"

    def __check(self, filepath: str):

        print(filepath)

        try:
            table = DBF(filepath, encoding=self.__encoding)
            num_records = len(table)
            first_record = next(iter(table))
            result = True
        except FileNotFoundError:
            print(f"❌ Ошибка: Файл '{filepath}' не найден.")
            result = False
        except Exception as e:
            # Ловим любые другие ошибки: поврежденный файл, проблемы с кодировкой и т.д.
            print(f"❌ Ошибка при чтении файла: {e}")
            print("   Возможно, файл поврежден или имеет неверную кодировку.")
            result =False
        finally:
            return result

    def check_file(self):
        try:
            self.__check(self._settings.altnames.path)
            self.__check(self._settings.doma.path)
            self.__check(self._settings.flat.path)
            self.__check(self._settings.kladr.path)
            self.__check(self._settings.namemap.path)
            self.__check(self._settings.socrbase.path)
            self.__check(self._settings.street.path)

            result = True
        except FileNotFoundError as e:
            print(f"❌ Ошибка: Файл '{e}' не найден.")
            result = False
        except Exception as e:
            # Ловим любые другие ошибки: поврежденный файл, проблемы с кодировкой и т.д.
            print(f"❌ Ошибка при чтении файла: {e}")
            print("   Возможно, файл поврежден или имеет неверную кодировку.")
            result =False
        finally:
            return result

class stream_dbf_loader(base_kladr):
    def __init__(self, file: str, table: str, queue: asyncio.Queue, conn_params: str):
        self._queue = queue
        self._conn_params = conn_params
        self._file = file
        self._table = table
        self._encoding = "cp866"
        self._batch_size_record = 100
    
    async def producer(self):
        try:
            file = DBF(self._file, encoding=self._encoding)

            batch = []
            count = 0

            for record in file:
                if count < self._batch_size_record:
                    batch.append(record)
                    count += 1
                else:
                    await self._queue.put(batch)
                    count = 0
                    batch = []

            await self._queue.put(batch)
            await self._queue.put(None)

        except Exception as e:
#            logger.error(f"{self.table_name}: Ошибка при чтении DBF: {e}")
            await self._queue.put(None)
            raise

    async def consumer(self):
        conn = None

        try:
            conn = await asyncpg.connect(self._conn_params)
            while True:
                batch = await self._queue.get()
                if batch is None:
                    break
                await self.batch_writer(conn, batch)
                self._queue.task_done()
            self._queue.task_done()

        except Exception as e:
#            logger.error(f"{self.table_name}: Ошибка при записи в БД: {e}")
            raise
        finally:
            if conn:
                await conn.close()

    async def batch_writer(self, conn: asyncpg.Connection, batch: List[Dict]):
        if not batch:
            return
        
        columns = list(batch[0].keys())

        rows = []

        for record in batch:
            row = [record[col] for col in columns]
            rows.append(row)


        async with conn.transaction():
            await conn.copy_records_to_table(
                self._table,
                columns=[col.lower() for col in columns],
                records=rows
            )

        # print(columns)
        # print(rows)

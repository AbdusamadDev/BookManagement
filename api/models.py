from dotenv import load_dotenv
from typing import Dict, List
import psycopg2
import re
import os

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path)


class Connection:
    def __init__(
        self, database: str, host: str, port: int, user: str, password: str
    ) -> None:
        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.cn = psycopg2.connect(
            user=self.user,
            database=self.database,
            host=self.host,
            port=self.port,
            password=self.password,
        )

    @property
    def cursor(self):
        return self.cn.cursor()

    @property
    def connection(self):
        return self.cn


class Database:
    DATATYPES = ["TEXT", "INTEGER", "JSON"]

    def __init__(self, name=None, fields: Dict = None) -> None:
        dbname = os.environ.get("DATABASE")
        user = os.environ.get("USER")
        password = os.environ.get("PASSWORD")
        host = os.environ.get("HOST")
        port = os.environ.get("PORT")
        self.name = name
        self.fields = fields
        self.connection = Connection(
            database=dbname, user=user, host=host, password=password, port=port
        )
        self.conn = self.connection.connection
        self.cursor = self.connection.cursor

    def createdb(self):
        fields = ""
        if self.name and fields is None:
            raise TypeError("name or fields attributes are not given")
        for key, value in self.fields.items():
            if not re.match(r"^[a-zA-Z]+$", key):
                raise TypeError(f"Field name is not valid: {key}")
            if value.upper() not in self.DATATYPES:
                raise TypeError(f"Datatype: {value} not valid for field: {key}")
            if 0 >= len(key) >= 200:
                raise NameError(f"Too long field name: {key[:20]}...")
            if not isinstance(key, str) or not isinstance(value, str):
                raise AttributeError("Fields can only be str!")
            fields += f"{key.lower()} {value.upper()},"
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS %s (%s)""" % (self.name, fields[:-1])
        )
        self.commit()

    def add(self, **kwargs):
        if self.name is None:
            raise TypeError("name parameter is not provided")
        fields = str(list(kwargs.keys()))[1:-1].replace('"', "").replace("'", "")
        values = str(list(kwargs.values()))[1:-1]
        self.cursor.execute(f"""INSERT INTO {self.name} ({fields}) VALUES ({values})""")
        self.commit()

    def commit(self):
        self.conn.commit()

    @property
    def fields(self) -> List:
        
        self.cursor.execute(
            f"""
            SELECT * FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = N'{self.name}'
            """
        )
        return [i[3] for i in self.cursor.fetchall()]


if __name__ == "__main__":
    database = Database(name="new_table", fields={"name": "Text", "age": "Integer"})
    database.createdb()
    database.add(name="Abdusamad", age=18)
    database.info()

from psycopg2.errors import SyntaxError as DBSyntaxError
from psycopg2 import OperationalError
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
    DATATYPES = ["TEXT", "INTEGER", "JSON", "SERIAL"]

    def __init__(self, name=None, fields: Dict = None, addons: str = "") -> None:
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
        self.addons = addons

    def createdb(self):
        fields = ""
        if self.name and fields is None:
            raise TypeError("name or fields attributes are not given")
        for key, value in self.fields.items():
            if not re.match(r'^[a-zA-Z_"]+$', key):
                raise TypeError(f"Field name is not valid: {key}")
            if value.upper().split(" ")[0] not in self.DATATYPES:
                raise TypeError(f"Datatype: {value} not valid for field: {key}")
            if 0 >= len(key) >= 200:
                raise NameError(f"Too long field name: {key[:20]}...")
            if not isinstance(key, str) or not isinstance(value, str):
                raise AttributeError("Fields can only be str!")
            fields += f"{key.lower()} {value.upper()},"
        try:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS %s (%s)"""
                % (self.name, fields[:-1] + ", " + self.addons)
            )
            self.commit()
        except DBSyntaxError as err:
            print(
                """CREATE TABLE IF NOT EXISTS %s (%s)"""
                % (self.name, fields[:-1] + ", " + self.addons)
            )
            raise TypeError("Database error: " + str(err))
    def add(self, **kwargs):
        if self.name is None:
            raise TypeError("name parameter is not provided")
        keys = list(kwargs.keys())

        def validate_fields(index):
            try:
                key = keys[index]
                index += 1
                if key not in self.columns:
                    raise Exception(f"Invalid column name: {key}")
            except IndexError:
                return None
            return validate_fields(index + 1)

        validate_fields(0)

        # Construct SQL query
        fields = ", ".join(keys)
        values = ", ".join(f"%({key})s" for key in keys)

        try:
            self.cursor.execute(
                f'''INSERT INTO {self.name} ({fields}) VALUES ({values})''',
                kwargs
            )
            self.commit()
        except OperationalError as err:
            raise Exception("Database error: ", str(err))




    def get(self, **field):
        self.cursor.execute(
            f"""SELECT * FROM {self.name} WHERE {list(field.keys())[0]}='{list(field.values())[0]}'"""
        )
        return self.cursor.fetchone()

    def commit(self):
        self.conn.commit()

    @property
    def columns(self) -> List:
        if self.name is None:
            raise TypeError("name parameter is not provided")
        self.cursor.execute(
            f"""
            SELECT * FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = N'{self.name}'
            """
        )
        return [i[3] for i in self.cursor.fetchall()]


if __name__ == "__main__":
    database = Database(
        name="another table", fields={"name": "Text NOT NULL", "age": "Integer"}
    )
    database.createdb()
    database.add(name="Abdusamad", age=18)

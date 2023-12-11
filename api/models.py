import psycopg2
from string import ascii_lowercase
import re

# from typing import


class Connection:
    def __init__(
        self, database: str, host: str, port: int, user: str, password: str
    ) -> None:
        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect(self):
        connection = psycopg2.connect(
            user=self.user,
            database=self.database,
            host=self.host,
            port=self.port,
            password=self.password,
        )
        return connection

    @property
    def cursor(self):
        connection = self.connect()
        return connection.cursor()

class Table:
    DATATYPES = ["TEXT", "INTEGER", "JSON"]

    def __init__(self, name, **fields) -> None:
        self.name = name
        self.fields = fields
        self.connection = Connection()
        self.cursor = self.connection.cursor

    def create(self):
        fields = ""
        for key, value in self.fields.items():
            if not re.match(r'^[a-zA-Z]+$', key):
                raise TypeError("Field name is not valid")
            if value not in self.DATATYPES:                  
                raise TypeError(f"Invalid datatype provided for field: {}")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS '%s' ()""")

    def close(self):
        pass

    # def create(self, )

import psycopg2
import re
import os
from dotenv import load_dotenv

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


class Table:
    DATATYPES = ["TEXT", "INTEGER", "JSON"]

    def __init__(self, name, **fields) -> None:
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

    def create(self):
        fields = ""
        for key, value in self.fields.items():
            if not re.match(r"^[a-zA-Z]+$", key):
                raise TypeError(f"Field name is not valid: {key}")
            if value not in self.DATATYPES:
                raise TypeError(f"Datatype: {value} not valid for field: {key}")
            if 0 >= len(key) >= 200:
                raise NameError(f"Too long field name: {key[:20]}...")
            if not isinstance(key, str) or not isinstance(value, str):
                raise AttributeError("Fields can only be str!")
            fields += f"{key.lower()}, {value.upper()}"
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS '%s' (%s);""" % (self.name, fields)
        )
        self.conn.commit()
        self.conn.close()

    def delete(self, name):
        query = f"SELECT {name} FROM information_schema.tables WHERE table_schema = 'public'"
        result_list = self.cursor.execute(query)
        print(result_list)


if __name__ == "__main__":
    database = Table("new_table", kwargs={"name": "TExt", "age": "Integer"})

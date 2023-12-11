import psycopg2


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
        psycopg2.connect(
            user=self.user,
            database=self.database,
            host=self.host,
            port=self.port,
            password=self.password,
        )


class Table:
    def __init__(self, name, **fields) -> None:
        self.name = name
        self.fields = fields
        self.connection = Connection()
        self.connection.connect()

    def create(self):
        pass

    def close(self):
        pass

    # def create(self, )

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

    def create_table(table):



class Table:
    def __init__(self, name, **fields) -> None:
        self.name = name
        self.fields = fields
        self.connection = Connection()

    def create(self):
        pass

    de


    # def create(self, )

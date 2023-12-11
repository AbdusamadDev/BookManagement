import psycopg2

# from typing import


class Connection:
    def __init__(
        self,
        database: str,
        host: str,
        port: int,
        user: str,
    ) -> None:
        pass


class Table:
    def __init__(self, name, **fields) -> None:
        self.name = name
        self.fields = fields

    # def create(self, )

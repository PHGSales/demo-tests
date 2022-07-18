from typing import Optional
from src.connection.connection_factory import ConnectionFactory


class User(object):
    def __init__(self, name: str, age: int, adress: str, connection: Optional[ConnectionFactory] = None):
        self.user_name = name
        self.age = age
        self.adress = adress
        self.table = "user_table"
        self.schema = "test"
        self.connection = connection or ConnectionFactory.build()

    def create(self):
        query = f"INSERT INTO {self.schema}.{self.table} values ('{self.user_name}', {self.age}, '{self.adress}')"
        return self.connection.run(query=query)

    def delete(self):
        query = f"DELETE FROM {self.schema}.{self.table} WHERE Name = '{self.user_name}'"
        return self.connection.run(query=query)

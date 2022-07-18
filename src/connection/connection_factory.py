from typing import Optional
import pymssql as pymssql


class ConnectionFactory(object):
    def __init__(self,
                 server: str,
                 database: str,
                 password: str,
                 user: str,
                 engine: Optional = None):
        self.server = server
        self.database = database
        self.password = password
        self.user = user
        self.cursor = None
        self.conn = None
        self.engine = engine or pymssql

    @staticmethod
    def build(engine: Optional = None):
        connection_factory = ConnectionFactory(server='localhost',
                                               database='master',
                                               password='@Sqlserver',
                                               user='sa',
                                               engine=engine)
        connection_factory._create_connection()
        return connection_factory

    def _create_connection(self):
        conn = self.engine.connect(self.server, self.user, self.password, self.database)
        self.cursor = conn.cursor()
        self.conn = conn

    def run(self, query: str):
        self.cursor.execute(query)
        self.conn.commit()

    def run_dql(self, query: str):
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        self.conn.commit()
        return row

    def close(self):
        return self.conn.close()

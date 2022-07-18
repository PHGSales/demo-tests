from unittest.mock import Mock
import pytest
from src.connection.connection_factory import ConnectionFactory

"""
Essa é a versão mockada dos testes.
"""


class TestConnectionFactory(object):
    @pytest.fixture
    def mocked_close(self):
        return Mock()

    @pytest.fixture
    def mocked_fetchall(self):
        return Mock()

    @pytest.fixture
    def mocked_commit(self):
        return Mock()

    @pytest.fixture
    def mocked_execute(self):
        return Mock()

    @pytest.fixture
    def mocked_cursor(self, mocked_fetchall, mocked_execute):
        mock = Mock()
        mock.execute = mocked_execute
        mock.fetchall = mocked_fetchall
        return mock

    @pytest.fixture
    def mocked_conn(self, mocked_cursor, mocked_commit, mocked_close):
        mock = Mock()
        mock.cursor = mocked_cursor
        mock.cursor.return_value = mocked_cursor
        mock.commit = mocked_commit
        mock.close = mocked_close
        return mock

    @pytest.fixture
    def mocked_engine(self, mocked_conn):
        mock = Mock()
        mock.connect = mocked_conn
        mock.connect.return_value = mocked_conn
        return mock

    @pytest.fixture
    def connection_factory(self, mocked_engine):
        connection_factory = ConnectionFactory(
            server="test_server",
            database="test_database",
            password="test_password",
            user="test_user",
            engine=mocked_engine)
        return connection_factory

    def test_build_should_return_a_connection(self, connection_factory, mocked_engine):
        connection = connection_factory.build(engine=mocked_engine)
        assert type(connection) == ConnectionFactory

    def test_create_connection_should_build_a_connection(self, connection_factory, mocked_engine, mocked_conn,
                                                         mocked_cursor):
        connection_factory._create_connection()
        assert connection_factory.conn == mocked_conn
        assert connection_factory.cursor == mocked_cursor

    def test_run_should_run_an_insert_into(self, connection_factory, mocked_cursor, mocked_conn):
        query = "INSERT INTO test.table values(123, 'test')"
        connection_factory._create_connection()
        connection_factory.run(query=query)
        connection_factory.cursor.execute.assert_called_once_with(query)
        connection_factory.conn.commit.assert_called_once_with()

    def test_run_dql_should_run_select_query(self, connection_factory, mocked_cursor, mocked_conn):
        query = "SELECT * FROM test.table"
        connection_factory._create_connection()
        connection_factory.run_dql(query=query)
        connection_factory.cursor.execute.assert_called_once_with(query)
        connection_factory.cursor.fetchall.assert_called_once_with()
        connection_factory.conn.commit.assert_called_once_with()

    def test_close_should_close_the_connection(self, connection_factory, mocked_engine, mocked_conn):
        connection = connection_factory.build(engine=mocked_engine)
        connection.close()
        connection.conn.close.assert_called_once_with()

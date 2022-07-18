from decimal import Decimal
import pytest
from pymssql import InterfaceError
from src.connection.connection_factory import ConnectionFactory

"""
Essa é a versão integrada dos testes. Você pode optar por fazer integrada ou mockada, mas sempre dê preferência a testes 
integrados, se for possível simular localmente os recursos necessários.
"""


class TestConnectionFactory(object):
    def setup_class(self):
        connection_factory = ConnectionFactory.build()
        connection_factory.run(query="CREATE SCHEMA test")
        connection_factory.run(
            query="CREATE TABLE test.user_table (Name varchar(50), Age numeric(3), Adress varchar(50))")

    def teardown_class(self):
        connection_factory = ConnectionFactory.build()
        connection_factory.run(query="DROP TABLE test.user_table")
        connection_factory.run(query="DROP SCHEMA test")
        connection_factory.conn.close()

    @pytest.fixture
    def connection_factory(self):
        return ConnectionFactory.build()

    def test_should_build_a_connection_builder_object(self):
        connection_factory = ConnectionFactory.build()
        assert type(connection_factory) == ConnectionFactory
        assert connection_factory.conn is not None
        assert connection_factory.cursor is not None

    def test_run_should_execute_a_insert_into_and_run_dql_execute_select(self, connection_factory):
        query = "INSERT INTO test.user_table values ('Maria', 15, 'Rua 123 de oliveira 4, n. 10')"
        connection_factory.run(query=query)
        row = connection_factory.run_dql(query="SELECT * FROM test.user_table WHERE Name = 'Maria'")
        assert row == [('Maria', Decimal('15'), 'Rua 123 de oliveira 4, n. 10')]

    def test_close_should_close_the_connection(self, connection_factory):
        query = "SELECT * FROM test.user_table"
        connection_factory.close()
        with pytest.raises(InterfaceError) as e:
            connection_factory.run(query=query)
        assert e.value.args[0] == 'Connection is closed.'


"""
Ponto 1: Não preciso fazer um teste especifico para o '_create_connection', 
pois ele já é executado no build e não tem como separar durante os testes. 
Por isso, testar somente o '_create_connection' seria reduntante. 

Ponto 2: No mesmo sentido, não é o ideal, mas como uso o 'run_dql' para validar o resultado do 'run',
então não preciso fazer um teste só para o 'run_dql', pois ele já está sendo testado."""

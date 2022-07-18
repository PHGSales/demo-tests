from decimal import Decimal
import pytest
from src.app.main import User
from src.connection.connection_factory import ConnectionFactory

"""
Alguns desses testes estão redundantes em relação ao testes do ConnectionFactory, pois eles acabam validando o 
comportamento de métodos que, indiretamente, já foram testados no 'test_connection_factory_2. A solução seria mockar a 
conexão com a 'ConnectionFactory', ou excluir os testes que estão redundantes. Porém, vou deixar aqui para exemplificar 
uma redundância.
"""


class TestUser(object):
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
    def user(self):
        return User(name="José da Silva",
                    age=18,
                    adress="Rua Maria da Silva, n 123, São Paulo-SP")

    def test_should_delete_user_row(self, user):
        user.create()
        row = user.connection.run_dql(query="SELECT * FROM test.user_table WHERE Name = 'José da Silva'")
        assert row == [('José da Silva', Decimal('18'), 'Rua Maria da Silva, n 123, São Paulo-SP')]
        user.delete()
        row = user.connection.run_dql(query="SELECT * FROM test.user_table WHERE Name = 'José da Silva'")
        assert row == []

    def test_should_insert_user_row(self, user):
        user.create()
        row = user.connection.run_dql(query="SELECT * FROM test.user_table WHERE Name = 'José da Silva'")
        assert row == [('José da Silva', Decimal('18'), 'Rua Maria da Silva, n 123, São Paulo-SP')]

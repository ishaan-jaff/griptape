import pytest
from griptape.drivers import SqlDriver
from griptape.loaders import SqlLoader

MAX_TOKENS = 50


class TestSqlLoader:
    @pytest.fixture
    def loader(self):
        sql_loader = SqlLoader(
            sql_driver=SqlDriver(
                engine_url="sqlite:///:memory:"
            )
        )

        sql_loader.sql_driver.execute_query(
            "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER, city TEXT);")
        sql_loader.sql_driver.execute_query(
            "INSERT INTO test_table (name, age, city) VALUES ('Alice', 25, 'New York');"
        )
        sql_loader.sql_driver.execute_query(
            "INSERT INTO test_table (name, age, city) VALUES ('Bob', 30, 'Los Angeles');"
        )
        sql_loader.sql_driver.execute_query(
            "INSERT INTO test_table (name, age, city) VALUES ('Charlie', 22, 'Chicago');"
        )

        return sql_loader

    def test_load(self, loader):
        result = loader.load("SELECT * FROM test_table;")

        assert len(result) == 3
        assert result[0].value == "1,Alice,25,New York"
        assert result[1].value == "2,Bob,30,Los Angeles"
        assert result[2].value == "3,Charlie,22,Chicago"
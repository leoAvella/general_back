import pytest
import os
from db import DBConnection

class TestDBConnection:
    # Tests that create_engine method successfully creates an engine
    def test_create_engine_success(self):
        db_connection = DBConnection()
        db_connection.create_engine()
        assert db_connection.engine is not None

    # Tests that create_engine method logs an exception when failing to create an engine
    def test_create_engine_failure(self, caplog):
        os.environ['DB_USER'] = 'invalid_user'
        os.environ['DB_PASSWORD'] = 'invalid_password'
        os.environ['DB_HOST'] = 'invalid_host'
        os.environ['DB_NAME'] = 'invalid_name'
        db_connection = DBConnection()
        db_connection.create_engine()
        assert db_connection.engine is None
        assert 'Failed to establish database connection' in caplog.text

    # Tests that get_db_connection method successfully gets a database connection
    def test_get_db_connection_success(self):
        db_connection = DBConnection()
        db_connection.create_engine()
        with db_connection.get_db_connection() as db:
            assert db is not None

    # Tests that get_db_connection method logs an exception when failing to get a database connection
    def test_get_db_connection_failure(self, caplog):
        os.environ['DB_USER'] = 'invalid_user'
        os.environ['DB_PASSWORD'] = 'invalid_password'
        os.environ['DB_HOST'] = 'invalid_host'
        os.environ['DB_NAME'] = 'invalid_name'
        db_connection = DBConnection()
        db_connection.create_engine()
        with db_connection.get_db_connection() as db:
            assert db is None
            assert 'Failed to establish database connection' in caplog.text

    # Tests that get_db_connection method handles exceptions when using database connection
    def test_get_db_connection_exception_handling(self, caplog):
        db_connection = DBConnection()
        db_connection.create_engine()
        with db_connection.get_db_connection() as db:
            try:
                raise Exception('Test exception')
            except Exception:
                pass
            assert 'An error occurred' in caplog.text

    # Tests that get_db_connection method closes database connection after use
    def test_get_db_connection_closing(self):
        db_connection = DBConnection()
        db_connection.create_engine()
        with db_connection.get_db_connection() as db:
            pass
        assert db.closed == True
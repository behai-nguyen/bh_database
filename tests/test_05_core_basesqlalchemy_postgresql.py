"""Test BaseSQLAlchemy class with PostgreSQL database.

To run only tests in this module: pytest -m base_model_postgresql
To run all tests with PostgreSQL database: pytest -k _postgresql_ -v
"""

import pytest

from sqlalchemy import (
    Column, 
    Integer,
)

from bh_database.core import (
    Database,
    BaseSQLAlchemy,
)

from tests import (
    POSTGRESQL_DB_URL,
    POSTGRESQL_DB_SCHEMA,
)

class PostgreSQLBaseTable(BaseSQLAlchemy):
    """Fictional, non existing table."""
    __tablename__ = 'test_postgresql'
    FICTIONAL_ID = Column( 'FICTIONAL_ID', Integer, primary_key=True )

@pytest.mark.base_model_postgresql
def test_postgresql_no_database():
    """Test a model class in initial state.

    No connection has been created. Scoped session and query are None.
    """

    assert PostgreSQLBaseTable.session == None
    assert PostgreSQLBaseTable.query == None

@pytest.mark.base_model_postgresql
def test_postgresql_class_connect_disconnect():
    """Test a model class after connect and disconnect.

    After connect, both class attributes session and query should be not None!

    After disconnect, both class attributes session and query should be None!
    """

    assert PostgreSQLBaseTable.session == None
    assert PostgreSQLBaseTable.query == None

    Database.connect(POSTGRESQL_DB_URL, POSTGRESQL_DB_SCHEMA)

    assert PostgreSQLBaseTable.session != None
    assert PostgreSQLBaseTable.query != None

    Database.disconnect()

    assert PostgreSQLBaseTable.session == None
    assert PostgreSQLBaseTable.query == None

@pytest.mark.base_model_postgresql
def test_postgresql_instance_connect_disconnect():
    """Test a model class after connect and disconnect.

    After connect, both class attributes session and query should be not None!

    After disconnect, both class attributes session and query should be None!
    After disconnect, both instance attributes session and query SHOULD BE 
    None: since the instance was created with default class attributes value.
    """

    assert PostgreSQLBaseTable.session == None
    assert PostgreSQLBaseTable.query == None

    Database.connect(POSTGRESQL_DB_URL, POSTGRESQL_DB_SCHEMA)

    assert PostgreSQLBaseTable.session != None
    assert PostgreSQLBaseTable.query != None

    """
    Instance is created with class attributes session and query default value.
    That is, the instance has not set values of these class attributes.
    """
    table = PostgreSQLBaseTable()
    assert table.session != None
    assert table.query != None

    Database.disconnect()

    assert PostgreSQLBaseTable.session == None
    assert PostgreSQLBaseTable.query == None

    """
    Instance was created with class attributes session and query default value.
    That is, the instance has not set values of these class attributes, any changes
    in the class will propagate back to those instances.
    """
    assert table.session == None
    assert table.query == None

@pytest.mark.base_model_postgresql
def test_postgresql_multiple_connect_disconnect():
    """Test multiple connect and disconnect calls.

    Class attributes value should change appropriately after each call.
    """

    assert PostgreSQLBaseTable.session == None
    assert PostgreSQLBaseTable.query == None

    Database.connect(POSTGRESQL_DB_URL, POSTGRESQL_DB_SCHEMA)

    assert PostgreSQLBaseTable.session != None
    assert PostgreSQLBaseTable.query != None

    Database.disconnect()

    assert PostgreSQLBaseTable.session == None
    assert PostgreSQLBaseTable.query == None

    Database.connect(POSTGRESQL_DB_URL, POSTGRESQL_DB_SCHEMA)

    assert PostgreSQLBaseTable.session != None
    assert PostgreSQLBaseTable.query != None

    Database.disconnect()

    assert PostgreSQLBaseTable.session == None
    assert PostgreSQLBaseTable.query == None

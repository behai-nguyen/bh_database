"""Test BaseSQLAlchemy class with MySQL database.

To run only tests in this module: pytest -m base_model_mysql
To run all tests with MySQL database: pytest -k _mysql_ -v
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

from tests import MYSQL_DB_URL

class MySQLBaseTable(BaseSQLAlchemy):
    """Fictional, non existing table."""
    __tablename__ = 'test_mysql'
    FICTIONAL_ID = Column( 'FICTIONAL_ID', Integer, primary_key=True )

@pytest.mark.base_model_mysql
def test_mysql_no_database():
    """Test a model class in initial state.

    No connection has been created. Scoped session and query are None.
    """

    assert MySQLBaseTable.session == None
    assert MySQLBaseTable.query == None

@pytest.mark.base_model_mysql
def test_mysql_class_connect_disconnect():
    """Test a model class after connect and disconnect.

    After connect, both class attributes session and query should be not None!

    After disconnect, both class attributes session and query should be None!
    """

    assert MySQLBaseTable.session == None
    assert MySQLBaseTable.query == None

    Database.connect(MYSQL_DB_URL, None)

    assert MySQLBaseTable.session != None
    assert MySQLBaseTable.query != None

    Database.disconnect()

    assert MySQLBaseTable.session == None
    assert MySQLBaseTable.query == None

@pytest.mark.base_model_mysql
def test_mysql_instance_connect_disconnect():
    """Test a model class after connect and disconnect.

    After connect, both class attributes session and query should be not None!

    After disconnect, both class attributes session and query should be None!
    After disconnect, both instance attributes session and query SHOULD BE 
    None: since the instance was created with default class attributes value.
    """

    assert MySQLBaseTable.session == None
    assert MySQLBaseTable.query == None

    Database.connect(MYSQL_DB_URL, None)

    assert MySQLBaseTable.session != None
    assert MySQLBaseTable.query != None

    """
    Instance is created with class attributes session and query default value.
    That is, the instance has not set values of these class attributes.
    """
    table = MySQLBaseTable()
    assert table.session != None
    assert table.query != None

    Database.disconnect()

    assert MySQLBaseTable.session == None
    assert MySQLBaseTable.query == None

    """
    Instance was created with class attributes session and query default value.
    That is, the instance has not set values of these class attributes, any changes
    in the class will propagate back to those instances.
    """
    assert table.session == None
    assert table.query == None

@pytest.mark.base_model_mysql
def test_mysql_multiple_connect_disconnect():
    """Test multiple connect and disconnect calls.

    Class attributes value should change appropriately after each call.
    """

    assert MySQLBaseTable.session == None
    assert MySQLBaseTable.query == None

    Database.connect(MYSQL_DB_URL, None)

    assert MySQLBaseTable.session != None
    assert MySQLBaseTable.query != None

    Database.disconnect()

    assert MySQLBaseTable.session == None
    assert MySQLBaseTable.query == None

    Database.connect(MYSQL_DB_URL, None)

    assert MySQLBaseTable.session != None
    assert MySQLBaseTable.query != None

    Database.disconnect()

    assert MySQLBaseTable.session == None
    assert MySQLBaseTable.query == None

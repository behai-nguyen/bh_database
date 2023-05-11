"""Test BaseTable, ReadOnlyTable, WriteCapableTable classes.

Test to ascertain certain behaviours of SQLAlchemy internal attributes.

These tests are not functionality tests.

To run only tests in this module: pytest -m base_table_mysql

To run all tests with MySQL database: pytest -k _mysql_ -v

On mysql() fixture:
-------------------

To ensure each test module can run independently and does not inadvertently produce
any side effects on later tests, or tests in other modules, the mysql() fixture needs 
to be called only once for this module.

The mysql() fixture establishes a connection to the underlying MySQL Employees Sample 
Database. This call is similar to applications establish database connection on starting up.
"""

from sqlalchemy import (
    Column, 
    Integer,
)

import pytest

from bh_database import core

from bh_database.base_table import (
    BaseTable,
    ReadOnlyTable,
    WriteCapableTable,
)

class MySQLBaseTable(BaseTable):
    """Fictional, non existing table."""
    __tablename__ = 'test_mysql1'
    FICTIONAL_ID = Column( 'FICTIONAL_ID', Integer, primary_key=True )

class MySQLReadOnlyTable(ReadOnlyTable):
    """Fictional, non existing table."""
    __tablename__ = 'test_mysql_read_only'
    FICTIONAL_ID = Column( 'FICTIONAL_ID', Integer, primary_key=True )

class MySQLWriteCapableTable(WriteCapableTable):
    """Fictional, non existing table."""
    __tablename__ = 'test_mysql_write_capable'
    FICTIONAL_ID = Column( 'FICTIONAL_ID', Integer, primary_key=True )

@pytest.mark.base_table_mysql
def test_mysql_prepare(mysql):
    """Database connection management.

    The purpose of this method is to establish the connection to the database.
    The mysql() method need to run FIRST and ONCE to establish the connection.

    I find this sort of work around is the most reliable method to control codes
    execution sequence.
    """

    assert core.BaseSQLAlchemy.session != None

    # BaseSQLAlchemy is abstract, with no table name.
    # ArgumentError("Column expression, FROM clause, or other columns clause element expected, 
    # got <class 'bh_database.core.BaseSQLAlchemy'>.")
    # assert core.BaseSQLAlchemy.query == None

@pytest.mark.base_table_mysql
def test_mysql_base_session():
    test = MySQLBaseTable()	
    assert (test.session is MySQLBaseTable.session) == True
    assert (test.session is BaseTable.session) == True
    assert id(test.session) == id(MySQLBaseTable.session)
    assert id(test.session) == id(BaseTable.session)

    test1 = MySQLBaseTable()	
    assert (test1.session is MySQLBaseTable.session) == True
    assert (test1.session is BaseTable.session) == True
    assert id(test1.session) == id(MySQLBaseTable.session)
    assert id(test1.session) == id(BaseTable.session)

    assert (test.session is test1.session) == True
    assert id(test.session) == id(test1.session)

@pytest.mark.base_table_mysql
def test_mysql_readonly_session():
    test = MySQLReadOnlyTable()	
    assert (test.session is MySQLReadOnlyTable.session) == True
    assert (test.session is BaseTable.session) == True
    assert id(test.session) == id(MySQLReadOnlyTable.session)
    assert id(test.session) == id(BaseTable.session)

    test1 = MySQLReadOnlyTable()	
    assert (test1.session is MySQLReadOnlyTable.session) == True
    assert (test1.session is BaseTable.session) == True
    assert id(test1.session) == id(MySQLReadOnlyTable.session)
    assert id(test1.session) == id(BaseTable.session)

    assert (test.session is test1.session) == True
    assert id(test.session) == id(test1.session)

@pytest.mark.base_table_mysql
def test_mysql_writecapable_session():
    test = MySQLWriteCapableTable()	
    assert (test.session is MySQLWriteCapableTable.session) == True
    assert (test.session is BaseTable.session) == True
    assert id(test.session) == id(MySQLWriteCapableTable.session)
    assert id(test.session) == id(BaseTable.session)

    test1 = MySQLWriteCapableTable()	
    assert (test1.session is MySQLWriteCapableTable.session) == True
    assert (test1.session is BaseTable.session) == True
    assert id(test1.session) == id(MySQLWriteCapableTable.session)
    assert id(test1.session) == id(BaseTable.session)

    assert (test.session is test1.session) == True
    assert id(test.session) == id(test1.session)

@pytest.mark.base_table_mysql
def test_mysql_base_query():
    # BaseTable is abstract with no table name.
    # ArgumentError("Column expression, FROM clause, or other columns clause element expected, 
    # got <class 'bh_database.core.BaseSQLAlchemy'>.")
    # assert BaseTable.query == None

    # MySQLBaseTable is not abstract, with a table name.
    assert MySQLBaseTable.query != None

    test = MySQLBaseTable()	
    assert test.query != None
    assert (test.query is MySQLBaseTable.query) == False
    assert id(test.query) != id(MySQLBaseTable.query)

    test1 = MySQLBaseTable()	
    assert (test1.query is MySQLBaseTable.query) == False
    assert id(test1.query) != id(MySQLBaseTable.query)

    assert (test.query is test1.query) == False
    assert id(test.query) != id(test1.query)

@pytest.mark.base_table_mysql 
def test_mysql_readonly_query():
    # ReadOnlyTable is abstract with no table name.
    # ArgumentError("Column expression, FROM clause, or other columns clause element expected, 
    # got <class 'bh_database.core.BaseSQLAlchemy'>.")
    # assert ReadOnlyTable.query == None

    # MySQLReadOnlyTable is not abstract, with a table name.
    assert MySQLReadOnlyTable.query != None

    test = MySQLReadOnlyTable()	
    assert test.query != None
    assert (test.query is MySQLReadOnlyTable.query) == False
    assert id(test.query) != id(MySQLReadOnlyTable.query)

    test1 = MySQLReadOnlyTable()	
    assert (test1.query is MySQLReadOnlyTable.query) == False
    assert id(test1.query) != id(MySQLReadOnlyTable.query)

    assert (test.query is test1.query) == False
    assert id(test.query) != id(test1.query)

@pytest.mark.base_table_mysql
def test_mysql_writecapable_query():
    # WriteCapableTable is abstract with no table name.
    # ArgumentError("Column expression, FROM clause, or other columns clause element expected, 
    # got <class 'bh_database.core.BaseSQLAlchemy'>.")
    # assert WriteCapableTable.query == None

    # MySQLWriteCapableTable is not abstract, with a table name.
    assert MySQLWriteCapableTable.query != None

    test = MySQLWriteCapableTable()	
    assert test.query != None
    assert (test.query is MySQLWriteCapableTable.query) == False
    assert id(test.query) != id(MySQLWriteCapableTable.query)

    test1 = MySQLWriteCapableTable()	
    assert (test1.query is MySQLWriteCapableTable.query) == False
    assert id(test1.query) != id(MySQLWriteCapableTable.query)

    assert (test.query is test1.query) == False
    assert id(test.query) != id(test1.query)

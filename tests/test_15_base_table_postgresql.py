"""Test BaseTable, ReadOnlyTable, WriteCapableTable classes.

Test to ascertain certain behaviours of SQLAlchemy internal attributes.

These tests are not functionality tests.

To run only tests in this module: pytest -m base_table_postgresql

To run all tests with PostgreSQL database: pytest -k _postgresql_ -v

On postgresql() fixture:
------------------------

To ensure each test module can run independently and does not inadvertently produce
any side effects on later tests, or tests in other modules, the postgresql() fixture
needs to be called only once for this module.

The postgresql() fixture establishes a connection to the underlying PostgreSQL 
Employees Sample Database. This call is similar to applications establish database
connection on starting up.
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

class PostgreSQLBaseTable(BaseTable):
    """Fictional, non existing table."""
    __tablename__ = 'test_postgresql1'
    FICTIONAL_ID = Column( 'FICTIONAL_ID', Integer, primary_key=True )

class PostgreSQLReadOnlyTable(ReadOnlyTable):
    """Fictional, non existing table."""
    __tablename__ = 'test_postgresql_read_only'
    FICTIONAL_ID = Column( 'FICTIONAL_ID', Integer, primary_key=True )

class PostgreSQLWriteCapableTable(WriteCapableTable):
    """Fictional, non existing table."""
    __tablename__ = 'test_postgresql_write_capable'
    FICTIONAL_ID = Column( 'FICTIONAL_ID', Integer, primary_key=True )

@pytest.mark.base_table_postgresql
def test_postgresql_prepare(postgresql):
    """Database connection management.

    The purpose of this method is to establish the connection to the database.
    The postgresql() method need to run FIRST and ONCE to establish the connection.

    I find this sort of work around is the most reliable method to control codes
    execution sequence.
    """

    assert core.BaseSQLAlchemy.session != None

    # BaseSQLAlchemy is abstract, with no table name.
    # ArgumentError("Column expression, FROM clause, or other columns clause element expected, 
    # got <class 'bh_database.core.BaseSQLAlchemy'>.")
    # assert core.BaseSQLAlchemy.query == None

@pytest.mark.base_table_postgresql
def test_postgresql_base_session():
    assert PostgreSQLBaseTable.session != None

    test = PostgreSQLBaseTable()	
    assert (test.session is PostgreSQLBaseTable.session) == True
    assert (test.session is BaseTable.session) == True
    assert id(test.session) == id(PostgreSQLBaseTable.session)
    assert id(test.session) == id(BaseTable.session)

    test1 = PostgreSQLBaseTable()	
    assert (test1.session is PostgreSQLBaseTable.session) == True
    assert (test1.session is BaseTable.session) == True
    assert id(test1.session) == id(PostgreSQLBaseTable.session)
    assert id(test1.session) == id(BaseTable.session)

    assert (test.session is test1.session) == True
    assert id(test.session) == id(test1.session)

@pytest.mark.base_table_postgresql
def test_postgresql_readonly_session():
    assert PostgreSQLReadOnlyTable.session != None

    test = PostgreSQLReadOnlyTable()	
    assert (test.session is PostgreSQLReadOnlyTable.session) == True
    assert (test.session is BaseTable.session) == True
    assert id(test.session) == id(PostgreSQLReadOnlyTable.session)
    assert id(test.session) == id(BaseTable.session)

    test1 = PostgreSQLReadOnlyTable()	
    assert (test1.session is PostgreSQLReadOnlyTable.session) == True
    assert (test1.session is BaseTable.session) == True
    assert id(test1.session) == id(PostgreSQLReadOnlyTable.session)
    assert id(test1.session) == id(BaseTable.session)

    assert (test.session is test1.session) == True
    assert id(test.session) == id(test1.session)

@pytest.mark.base_table_postgresql
def test_postgresql_writecapable_session():
    assert PostgreSQLWriteCapableTable.session != None

    test = PostgreSQLWriteCapableTable()	
    assert (test.session is PostgreSQLWriteCapableTable.session) == True
    assert (test.session is BaseTable.session) == True
    assert id(test.session) == id(PostgreSQLWriteCapableTable.session)
    assert id(test.session) == id(BaseTable.session)

    test1 = PostgreSQLWriteCapableTable()	
    assert (test1.session is PostgreSQLWriteCapableTable.session) == True
    assert (test1.session is BaseTable.session) == True
    assert id(test1.session) == id(PostgreSQLWriteCapableTable.session)
    assert id(test1.session) == id(BaseTable.session)

    assert (test.session is test1.session) == True
    assert id(test.session) == id(test1.session)

@pytest.mark.base_table_postgresql
def test_postgresql_base_query():
    
    # BaseTable is abstract with no table name.
    # ArgumentError("Column expression, FROM clause, or other columns clause element expected, 
    # got <class 'bh_database.core.BaseSQLAlchemy'>.")
    # assert BaseTable.query == None

    # PostgreSQLBaseTable is not abstract, with a table name.
    assert PostgreSQLBaseTable.query != None

    test = PostgreSQLBaseTable()	
    assert test.query != None
    assert (test.query is PostgreSQLBaseTable.query) == False
    assert id(test.query) != id(PostgreSQLBaseTable.query)

    test1 = PostgreSQLBaseTable()	
    assert (test1.query is PostgreSQLBaseTable.query) == False
    assert id(test1.query) != id(PostgreSQLBaseTable.query)

    assert (test.query is test1.query) == False
    assert id(test.query) != id(test1.query)

@pytest.mark.base_table_postgresql 
def test_postgresql_readonly_query():

    # ReadOnlyTable is abstract with no table name.
    # ArgumentError("Column expression, FROM clause, or other columns clause element expected, 
    # got <class 'bh_database.core.BaseSQLAlchemy'>.")
    # assert ReadOnlyTable.query == None

    # PostgreSQLReadOnlyTable is not abstract, with a table name.
    assert PostgreSQLReadOnlyTable.query != None

    test = PostgreSQLReadOnlyTable()	
    assert test.query != None
    assert (test.query is PostgreSQLReadOnlyTable.query) == False
    assert id(test.query) != id(PostgreSQLReadOnlyTable.query)

    test1 = PostgreSQLReadOnlyTable()	
    assert (test1.query is PostgreSQLReadOnlyTable.query) == False
    assert id(test1.query) != id(PostgreSQLReadOnlyTable.query)

    assert (test.query is test1.query) == False
    assert id(test.query) != id(test1.query)

@pytest.mark.base_table_postgresql
def test_postgresql_writecapable_query():
    # WriteCapableTable is abstract with no table name.
    # ArgumentError("Column expression, FROM clause, or other columns clause element expected, 
    # got <class 'bh_database.core.BaseSQLAlchemy'>.")
    # assert WriteCapableTable.query == None

    # PostgreSQLWriteCapableTable is not abstract, with a table name.
    assert PostgreSQLWriteCapableTable.query != None

    test = PostgreSQLWriteCapableTable()	
    assert test.query != None
    assert (test.query is PostgreSQLWriteCapableTable.query) == False
    assert id(test.query) != id(PostgreSQLWriteCapableTable.query)

    test1 = PostgreSQLWriteCapableTable()	
    assert (test1.query is PostgreSQLWriteCapableTable.query) == False
    assert id(test1.query) != id(PostgreSQLWriteCapableTable.query)

    assert (test.query is test1.query) == False
    assert id(test.query) != id(test1.query)

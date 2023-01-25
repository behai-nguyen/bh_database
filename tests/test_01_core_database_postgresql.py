"""Test Database "static" class with PostgreSQL database.

To run only tests in this module: pytest -m database_postgresql

To run all tests with PostgreSQL database: pytest -k _postgresql_ -v
"""

import pytest

from sqlalchemy import text

from bh_database.core import (
    Database,
    DatabaseType,
    BaseQuery,
)

from tests import (
    POSTGRESQL_DB_URL,
    POSTGRESQL_DB_SCHEMA,
)
from tests.employees import (
    SELECT_EMPLOYEES,
    assert_employees_list_of_tuples,
)

@pytest.mark.database_postgresql
def test_postgresql_no_connection():
    """Test Database class in initial state.

    No connection has been created. All database classes are None.
    """

    """
    Getting rid of any residual connection from previous test runs.
    """
    Database.disconnect()

    assert Database.engine == None
    assert Database.session_factory == None
    assert Database.database_session == None

@pytest.mark.database_postgresql
def test_postgresql_auxilary_functions():
    """Test Database methods Database.database_type(db_url=None) and 
    Database.driver_name()
    """

    """
    Getting rid of any residual connection from previous test runs.
    """
    Database.disconnect()
    Database.connect(POSTGRESQL_DB_URL, POSTGRESQL_DB_SCHEMA)
    assert Database.database_type() == DatabaseType.PostgreSQL
    assert Database.driver_name() == 'postgresql+psycopg2'

    Database.disconnect()
    assert Database.database_type(POSTGRESQL_DB_URL) == DatabaseType.PostgreSQL

    """
    Database.database_type(db_url=None) only works in disconnected if db_url is specified.
    """
    error = False
    except_msg = ""
    try:
        Database.database_type()
    except Exception as e:
        error = True
        except_msg = str(e)

    assert error == True
    assert len(except_msg) > 0

    """
    Database.driver_name() only works if connected to a database server.
    """
    error = False
    except_msg = ""
    try:
        Database.driver_name()
    except Exception as e:
        error = True
        except_msg = str(e)

    assert error == True
    assert len(except_msg) > 0

@pytest.mark.database_postgresql
def test_postgresql_connect():
    """Ascertain some basic behaviours: 
    
        -- Calling Database.disconnect(), core database classes set to None, 
            all connections closed. But scoped sessions and query created locally 
            are still not None.
    """

    """
    Getting rid of any residual connection from previous test runs.
    """
    Database.disconnect()

    Database.connect(POSTGRESQL_DB_URL, POSTGRESQL_DB_SCHEMA)

    assert Database.engine != None
    assert Database.session_factory != None
    assert Database.database_session != None

    session = Database.database_session()
    query = Database.database_session.query_property(BaseQuery)
    other_session = Database.database_session()

    assert session != None
    assert query != None
    assert other_session != None

    assert (other_session is session) == True

    Database.disconnect()

    assert Database.engine == None
    assert Database.session_factory == None
    assert Database.database_session == None

    assert session != None
    assert query != None
    assert other_session != None

@pytest.mark.database_postgresql
def test_postgresql_create_invalid():
    """Test connecting to a PostgreSQL database with an invalid database URL.

    The call should raise an exception, callers must handle the exception.
    """
    Database.disconnect()

    error = False
    exception_msg = ""
    try:
        Database.connect(POSTGRESQL_DB_URL + "xxx", POSTGRESQL_DB_SCHEMA)
    except Exception as e:
        error = True
        exception_msg = str(e)

    assert error == True
    assert len(exception_msg) > 0

    print(exception_msg)

@pytest.mark.database_postgresql
def test_postgresql_scoped_session_select():
    """Connect to PostgreSQL "employees" database and select some data.

    Test the behaviours of a locally created scoped session: run a full
    text query statement with it.
    """
    Database.disconnect()

    Database.connect(POSTGRESQL_DB_URL, POSTGRESQL_DB_SCHEMA)

    session = Database.database_session()

    result = session.execute(text(SELECT_EMPLOYEES))
    # result is CursorResult.
    assert result.rowcount == 38

    assert_employees_list_of_tuples(result.fetchall())

    Database.disconnect()

@pytest.mark.database_postgresql
def test_postgresql_use_session_after_disconnect():
    """Ascertain some basic behaviours.
	
        Recall from test_postgresql_connect():
    
        -- Calling Database.disconnect(), core database classes set to None, 
            all connections closed. But scoped sessions and query created locally 
            are still not None.

    This test proves that locally created scoped sessions are still valid, and
    can be used to query data!
    """

    Database.connect(POSTGRESQL_DB_URL, POSTGRESQL_DB_SCHEMA)

    session = Database.database_session()
    query = Database.database_session.query_property(BaseQuery)
    other_session = Database.database_session()

    Database.disconnect()

    assert session != None
    assert query != None
    assert other_session != None

    result = session.execute(text(SELECT_EMPLOYEES))
    # result is CursorResult.
    assert result.rowcount == 38

    assert_employees_list_of_tuples(result.fetchall())

    result = other_session.execute(text(SELECT_EMPLOYEES))
    # result is CursorResult.
    assert result.rowcount == 38

    assert_employees_list_of_tuples(result.fetchall())
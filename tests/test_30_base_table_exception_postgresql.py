"""Test BaseTable, ReadOnlyTable, WriteCapableTable classes.

These are still CRUD functionality tests.

Asserts that database violations, e.g. duplicate key value, etc., are 
propagated out to the exception handling block of the respective methods.

To run only tests in this module: pytest -m base_table_exception_postgresql

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

from http import HTTPStatus
import datetime
import pytest

from bh_database import core
from bh_database.constant import (
    BH_REC_STATUS_FIELDNAME,
    BH_RECORD_STATUS_NEW,
)

from tests.employees import Employees

@pytest.mark.base_table_exception_postgresql
def test_postgresql_prepare(postgresql):
    """Database connection management.

    The purpose of this method is to establish the connection to the database.
    The postgresql() method need to run FIRST and ONCE to establish the connection.

    I find this sort of work around is the most reliable method to control codes
    execution sequence.
    """

    assert core.BaseSQLAlchemy.session != None
    # BaseSQLAlchemy is abstract, with no table name.
    assert core.BaseSQLAlchemy.query == None

@pytest.mark.base_table_exception_postgresql
def test_postgresql_write_to_database_exception():
    """Insert two records, one after the other, with duplicate primary key,
    the second one should fail, exception should be handled.

    Test that the second insert failed and status code is 500.
    """
	
    MAGIC_NEW_EMP_NO = 1000000

    """
    Remove the test employee to be on the safe side.
    """
    Employees.begin_transaction(Employees)
    Employees.query.filter(Employees.emp_no==MAGIC_NEW_EMP_NO).delete()
    Employees.commit_transaction(Employees)

    """
    First new employee: note 'emp_no' specified!
    """
    new_employee = {
        'emp_no': MAGIC_NEW_EMP_NO,
        'birth_date': '1975-08-23',
        'first_name': 'John',
        'last_name': 'Smith',
        'gender': 'M',
        'hire_date': '2010-11-29',
        BH_REC_STATUS_FIELDNAME: BH_RECORD_STATUS_NEW}		
    
    """
    This insert should go through successfully.
    """
    employees = Employees()
    employees.begin_transaction()
    status = employees.write_to_database([new_employee])
    employees.finalise_transaction(status)

    assert status.code == HTTPStatus.OK.value

    """
    ACTUAL TEST: insert another new employee with the same primary key as the first one.
    """
    """
    Second new employee with duplicate primary key.
    """
    new_employee = {
        'emp_no': MAGIC_NEW_EMP_NO,
        'birth_date': '1965-01-2',
        'first_name': 'Don',
        'last_name': 'Tran',
        'gender': 'M',
        'hire_date': '2012-1-22',
        BH_REC_STATUS_FIELDNAME: BH_RECORD_STATUS_NEW}    

    employees = Employees()
    employees.begin_transaction()
    status = employees.write_to_database([new_employee])
    employees.finalise_transaction(status)

    assert status.code == HTTPStatus.INTERNAL_SERVER_ERROR.value

    """
    Assert the first successful inserted employee actually exists in database.
    """
    result = Employees.query.filter(Employees.emp_no==MAGIC_NEW_EMP_NO)
    assert result.count() == 1
    record = result.first()
    assert record.emp_no == MAGIC_NEW_EMP_NO
    assert record.birth_date == datetime.date(1975, 8, 23) 
    assert record.first_name == 'John'
    assert record.last_name == 'Smith'
    assert record.gender == 'M'
    assert record.hire_date == datetime.date(2010, 11, 29)

    """
    Remove the first successful inserted employee.
    """
    Employees.begin_transaction(Employees)
    Employees.query.filter(Employees.emp_no==MAGIC_NEW_EMP_NO).delete()
    Employees.commit_transaction(Employees)
"""Test BaseTable, ReadOnlyTable, WriteCapableTable classes.

These tests are CRUD functionality tests.

To run only tests in this module: pytest -m base_table_crud_mysql

To run all tests with MySQL database: pytest -k _mysql_ -v

On mysql() fixture:
-------------------

To ensure each test module can run independently and does not inadvertently produce
any side effects on later tests, or tests in other modules, the mysql() fixture needs 
to be called only once for this module.

The mysql() fixture establishes a connection to the underlying MySQL Employees Sample 
Database. This call is similar to applications establish database connection on starting up.
"""

from http import HTTPStatus
import datetime
import pytest

from bh_database import core
from bh_database.constant import (
    BH_REC_STATUS_FIELDNAME,
    BH_RECORD_STATUS_NEW,
    BH_RECORD_STATUS_MODIFIED,
)

from tests.employees import (
    Employees,
    SELECT_EMPLOYEES,
    assert_employees_list_of_dicts,
)

@pytest.mark.base_table_crud_mysql
def test_mysql_prepare(mysql):
    """Database connection management.

    The purpose of this method is to establish the connection to the database.
    The postgresql() method need to run FIRST and ONCE to establish the connection.

    I find this sort of work around is the most reliable method to control codes
    execution sequence.
    """

    assert core.BaseSQLAlchemy.session != None
    # BaseSQLAlchemy is abstract, with no table name.
    assert core.BaseSQLAlchemy.query == None

@pytest.mark.base_table_crud_mysql
def test_mysql_run_select_sql():
    """Test a full text SELECT SQL statement.
    """

    employees = Employees()
    status = employees.run_select_sql(SELECT_EMPLOYEES, True)

    assert status.code == HTTPStatus.OK.value
    assert len(status.text) > 0
    assert hasattr(status, 'data') == True
    assert len(status.data) == 38

    assert_employees_list_of_dicts(status.data)

@pytest.mark.base_table_crud_mysql
def test_mysql_write_to_database_commit_01():
    """Test transaction atomicity.

    Test insert a new record then commit.
    """

    """
    Note there is no 'emp_no' specified.
    """
    new_employee = {'birth_date': '1967-09-11',
        'first_name': 'Be Hai',
        'last_name': 'Nguyen',
        'gender': 'F',
        'hire_date': '2022-09-11',
        BH_REC_STATUS_FIELDNAME: BH_RECORD_STATUS_NEW}
    
    employees = Employees()

    """
    Transaction atomicity -- if there are other operations, they are wrapped within:
        employees.begin_transaction() or Employees.begin_transaction(Employees)
        ...
        employees.commit_transaction() Employees.commit_transaction(Employees)

    Of course, employees.commit_transaction() / Employees.commit_transaction(Employees) 
    should be called conditionally.
    """
    employees.begin_transaction()
    status = employees.write_to_database([new_employee])
    """
    Commit transaction: it should be called on successful completion of all writes.
    """    
    employees.commit_transaction()

    assert status.code == HTTPStatus.OK.value
    assert len(status.text) > 0
    assert hasattr(status, 'data') == True

    assert hasattr(status.data, 'employees_new_list') == True
    assert hasattr(status.data, 'employees_updated_list') == True

    """
    There is one (1) new record.
    There is no updated record.
    """
    assert len(status.data.employees_new_list) == 1
    assert len(status.data.employees_updated_list) == 0

    new_emp_no = status.data.employees_new_list[0]['emp_no']
    """
    499999 is the last emp_no in the original test data.
    """
    assert new_emp_no > 499999

    """
    Read the newly inserted employee back and verify data inserted.
    """
    result = Employees.query.filter(Employees.emp_no==new_emp_no)

    assert result.count() == 1

    record = result.first()
    assert record.emp_no == new_emp_no
    assert record.birth_date == datetime.date(1967, 9, 11) 
    assert record.first_name == 'Be Hai'
    assert record.last_name == 'Nguyen'
    assert record.gender == 'F'
    assert record.hire_date == datetime.date(2022, 9, 11)

    """
    Remove the newly inserted employee.
    """
    Employees.begin_transaction(Employees)
    Employees.query.filter(Employees.emp_no==new_emp_no).delete()
    Employees.commit_transaction(Employees)

    """
    Verify that it has been removed.
    """
    result = Employees.query.filter(Employees.emp_no==new_emp_no)
    assert result.count() == 0

@pytest.mark.base_table_crud_mysql
def test_mysql_write_to_database_commit_02():
    """Test transaction atomicity.

    Test insert two new records: one without a primary key, one with primary key.
    """
	
    MAGIC_NEW_EMP_NO = 1000000

    """
    Note there is no 'emp_no' specified.
    """
    new_employee1 = {'birth_date': '1967-09-11',
        'first_name': 'Be Hai',
        'last_name': 'Nguyen',
        'gender': 'F',
        'hire_date': '2022-09-11',
        BH_REC_STATUS_FIELDNAME: BH_RECORD_STATUS_NEW}
		
    """
    Note there is 'emp_no' specified!
    """
    new_employee2 = {
        'emp_no': MAGIC_NEW_EMP_NO,
        'birth_date': '1975-08-23',
        'first_name': 'John',
        'last_name': 'Smith',
        'gender': 'M',
        'hire_date': '2010-11-29',
        BH_REC_STATUS_FIELDNAME: BH_RECORD_STATUS_NEW}		
    
    """
    Transaction atomicity -- if there are other operations, they are wrapped within:
        Employees.begin_transaction(Employees)
        ...
        Employees.commit_transaction(Employees)

    Of course, Employees.commit_transaction(Employees) should be called conditionally.
    """
    Employees.begin_transaction(Employees)
    status = Employees().write_to_database([new_employee1, new_employee2])
    """
    Commit transaction: it should be called on successful completion of all writes.
    """    
    Employees.commit_transaction(Employees)

    assert status.code == HTTPStatus.OK.value
    assert len(status.text) > 0
    assert hasattr(status, 'data') == True

    assert hasattr(status.data, 'employees_new_list') == True
    assert hasattr(status.data, 'employees_updated_list') == True

    """
    There are two (2) new records.
    There is no updated record.
    """
    assert len(status.data.employees_new_list) == 2
    assert len(status.data.employees_updated_list) == 0

    new_emp_no = status.data.employees_new_list[0]['emp_no']
    """
    499999 is the last emp_no in the original test data.
    """
    assert new_emp_no > 499999
    assert status.data.employees_new_list[1]['emp_no'] == MAGIC_NEW_EMP_NO

    """
    Read the newly inserted employees back and verify data inserted.
    """
    result = Employees.query.filter(Employees.emp_no==new_emp_no)

    assert result.count() == 1

    record = result.first()
    assert record.emp_no == new_emp_no
    assert record.birth_date == datetime.date(1967, 9, 11) 
    assert record.first_name == 'Be Hai'
    assert record.last_name == 'Nguyen'
    assert record.gender == 'F'
    assert record.hire_date == datetime.date(2022, 9, 11)

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
    Remove the newly inserted employees.
    """
    Employees.begin_transaction(Employees)
    Employees.query.filter(Employees.emp_no==new_emp_no).delete()
    Employees.query.filter(Employees.emp_no==MAGIC_NEW_EMP_NO).delete()
    Employees.commit_transaction(Employees)

    """
    Verify that newly inserted employees have been removed.
    """
    result = Employees.query.filter(Employees.emp_no==new_emp_no)
    assert result.count() == 0
    result = Employees.query.filter(Employees.emp_no==MAGIC_NEW_EMP_NO)
    assert result.count() == 0

@pytest.mark.base_table_crud_mysql
def test_mysql_write_to_database_commit_03():
    """Test transaction atomicity.

    Test insert a new record, update an existing record, then commit.
    """

    """
    Create a new record which is to be updated.
    Note there is no 'emp_no' specified.
    """
    new_employee = {'birth_date': '1967-09-11',
        'first_name': 'Be Hai',
        'last_name': 'Nguyen',
        'gender': 'F',
        'hire_date': '2022-09-11',
        BH_REC_STATUS_FIELDNAME: BH_RECORD_STATUS_NEW}
    
    """
    Transaction atomicity -- if there are other operations, they are wrapped within:
        Employees.begin_transaction(Employees)
        ...
        Employees.commit_transaction(Employees)

    Of course, employees.commit_transaction() / Employees.commit_transaction(Employees) 
    should be called conditionally.
    """
    Employees.begin_transaction(Employees)
    status = Employees().write_to_database([new_employee])
    """
    Commit transaction: it should be called on successful completion of all writes.
    """    
    Employees.commit_transaction(Employees)

    assert status.code == HTTPStatus.OK.value

    new_emp_no_1 = status.data.employees_new_list[0]['emp_no']

    """
    Updated record.
    Note the presence of 'emp_no'.
    """
    updated_employee = {
        'emp_no': new_emp_no_1,
        'first_name': 'Văn Bé Hai',
        'last_name': 'Nguyễn',
        'gender': 'M',
        BH_REC_STATUS_FIELDNAME: BH_RECORD_STATUS_MODIFIED}
    
    """
    New record.
    Note there is no 'emp_no' specified.
    """
    new_employee = {'birth_date': '1975-08-23',
        'first_name': 'John',
        'last_name': 'Smith',
        'gender': 'M',
        'hire_date': '2010-11-29',
        BH_REC_STATUS_FIELDNAME: BH_RECORD_STATUS_NEW}
    
    Employees.begin_transaction(Employees)
    status = Employees().write_to_database([new_employee, updated_employee])
    """
    Commit transaction: it should be called on successful completion of all writes.
    """    
    Employees.commit_transaction(Employees)

    assert status.code == HTTPStatus.OK.value
    assert len(status.text) > 0
    assert hasattr(status, 'data') == True

    assert hasattr(status.data, 'employees_new_list') == True
    assert hasattr(status.data, 'employees_updated_list') == True

    assert len(status.data.employees_new_list) == 1
    assert len(status.data.employees_updated_list) == 1

    updated_emp = status.data.employees_updated_list[0]
    new_emp = status.data.employees_new_list[0]

    new_emp_no_2 = new_emp['emp_no']

    assert (new_emp_no_2 - new_emp_no_1) == 1

    assert updated_emp['emp_no'] == new_emp_no_1
    # assert updated_emp['birth_date'] == datetime.date(1967, 9, 11) 
    assert updated_emp['first_name'] == 'Văn Bé Hai'
    assert updated_emp['last_name'] == 'Nguyễn'
    assert updated_emp['gender'] == 'M'
    # assert updated_emp['hire_date'] == datetime.date(2022, 9, 11)

    assert new_emp['birth_date'] == '1975-08-23'
    assert new_emp['first_name'] == 'John'
    assert new_emp['last_name'] == 'Smith'
    assert new_emp['gender'] == 'M'
    assert new_emp['hire_date'] == '2010-11-29'

    """
    Read out of database, and test individually.
    """
    result = Employees.query.filter(Employees.emp_no==new_emp_no_1)
    assert result.count() == 1
    record = result.first()
    assert record.emp_no == new_emp_no_1
    assert record.birth_date == datetime.date(1967, 9, 11) 
    assert record.first_name == 'Văn Bé Hai'
    assert record.last_name == 'Nguyễn'
    assert record.gender == 'M'
    assert record.hire_date == datetime.date(2022, 9, 11)

    result = Employees.query.filter(Employees.emp_no==new_emp_no_2)
    assert result.count() == 1
    record = result.first()
    assert record.emp_no == new_emp_no_2
    assert record.birth_date == datetime.date(1975, 8, 23) 
    assert record.first_name == 'John'
    assert record.last_name == 'Smith'
    assert record.gender == 'M'
    assert record.hire_date == datetime.date(2010, 11, 29)

    """
    Remove both.
    """
    Employees.begin_transaction(Employees)
    Employees.query.filter(Employees.emp_no==new_emp_no_1).delete()
    Employees.query.filter(Employees.emp_no==new_emp_no_2).delete()
    Employees.commit_transaction(Employees)

@pytest.mark.base_table_crud_mysql
def test_mysql_write_to_database_flush_and_rollback():
    """Test transaction atomicity.
    
    Test insert a new record, flush the transaction to get the unique primary key value,
    then rollback the transaction, finally verify that the transaction has been rolled back
    by querying for the just rolled back employee using the intermediate primary key value
    obtained after flushing the transaction.
    """

    """
    Note there is no 'emp_no' specified.
    """
    new_employee = {'birth_date': '1967-09-11',
        'first_name': 'Be Hai',
        'last_name': 'Nguyen',
        'gender': 'F',
        'hire_date': '2022-09-11',
        BH_REC_STATUS_FIELDNAME: BH_RECORD_STATUS_NEW}
    
    """
    Transaction atomicity -- if there are other operations, they are wrapped within:
        employees.begin_transaction() or Employees.begin_transaction(Employees)
        ...
        employees.commit_transaction() or Employees.rollback_transaction(Employees)

    Of course, Employees.rollback_transaction(Employees) should be called conditionally.
    """
    Employees.begin_transaction(Employees)
    status = Employees().write_to_database([new_employee])
    """
    Flush transaction so intermediate result is available.
    """    
    Employees.flush_transaction(Employees)
    """
    Remember the employee number of the newly inserted employee, which is going to be
    rolled back.
    """
    new_emp_no = status.data.employees_new_list[0]['emp_no']

    """
    Rollback transaction: it should be called on some failure condition.
    """
    Employees.rollback_transaction(Employees)

    assert status.code == HTTPStatus.OK.value
    assert len(status.text) > 0

    """
    499999 is the last emp_no in the original test data.
    """
    assert new_emp_no > 499999

    """
    Verify that it has been rolled back.
    """
    result = Employees.query.filter(Employees.emp_no==new_emp_no)
    assert result.count() == 0

@pytest.mark.base_table_crud_mysql
def test_mysql_run_execute_sql():
    """Test a full text UPDATE SQL statement.

    Insert a new test record. Then update some fields with via a full text 
    UPDATE SQL statement.
    """

    """
    Note there is no 'emp_no' specified.
    """
    new_employee = {'birth_date': '1967-09-11',
        'first_name': 'Be Hai',
        'last_name': 'Nguyen',
        'gender': 'F',
        'hire_date': '2022-09-11',
        BH_REC_STATUS_FIELDNAME: BH_RECORD_STATUS_NEW}
    
    """
    Transaction atomicity -- if there are other operations, they are wrapped within:
        employees.begin_transaction() or Employees.begin_transaction(Employees)
        ...
        employees.commit_transaction() Employees.commit_transaction(Employees)

    Of course, employees.commit_transaction() / Employees.commit_transaction(Employees) 
    should be called conditionally.
    """
    Employees.begin_transaction(Employees)
    status = Employees().write_to_database([new_employee])
    """
    Commit transaction: it should be called on successful completion of all writes.
    """    
    Employees.commit_transaction(Employees)

    new_emp_no = status.data.employees_new_list[0]['emp_no']

    """
    Read the newly inserted employee back and verify data inserted.
    We are only interested in the fields we are going to update.
    """
    result = Employees.query.filter(Employees.emp_no==new_emp_no)

    assert result.count() == 1

    record = result.first()
    assert record.first_name == 'Be Hai'
    assert record.last_name == 'Nguyen'
    assert record.gender == 'F'

    """
    ACTUAL TEST STARTS.
    """
    update_sql = ( "update employees set first_name = 'Văn Bé Hai', last_name = 'Nguyễn', "\
                  f"gender = 'M' where emp_no = {new_emp_no}")
    
    status = Employees().run_execute_sql(update_sql, True)

    assert status.code == HTTPStatus.OK.value
    assert hasattr(status, 'data') == True
    assert status.data == None

    """
    Read the newly updated employee back and verify data updated.
    """
    result = Employees.query.filter(Employees.emp_no==new_emp_no)

    assert result.count() == 1

    record = result.first()
    assert record.emp_no == new_emp_no
    assert record.birth_date == datetime.date(1967, 9, 11) 
    assert record.first_name == 'Văn Bé Hai'
    assert record.last_name == 'Nguyễn'
    assert record.gender == 'M'
    assert record.hire_date == datetime.date(2022, 9, 11)

    """
    Remove the newly inserted employee.
    """
    Employees.begin_transaction(Employees)
    Employees.query.filter(Employees.emp_no==new_emp_no).delete()
    Employees.commit_transaction(Employees)

    """
    Verify that it has been removed.
    """
    result = Employees.query.filter(Employees.emp_no==new_emp_no)
    assert result.count() == 0

@pytest.mark.base_table_crud_mysql
def test_mysql_run_stored_proc():
    """Test running a stored procedure which returns a dataset.

    The stored procedure is get_employees(...).
    """

    """
    auto_session=True is because this is a simple select stored procedure, 
    we don't need transaction atomicity.
    """
    status = Employees().run_stored_proc("get_employees", ["%nas%", "%an"], auto_session=True)

    assert status.code == HTTPStatus.OK.value
    assert len(status.text) > 0
    assert hasattr(status, 'data') == True
    assert len(status.data) == 38

    assert_employees_list_of_dicts(status.data)

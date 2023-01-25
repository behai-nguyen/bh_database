"""Test BaseTable, ReadOnlyTable, WriteCapableTable classes.

Tests for the __init__(self, **kwargs) and the as_dict(self) -> dict methods.

These tests are database neutral and don't require a database connection.

To run only tests in this module: pytest -m base_table_methods

To run all tests with PostgreSQL database: pytest -k _postgresql_ -v
To run all tests with MySQL database: pytest -k _mysql_ -v
"""

import pytest

from tests.employees import Employees

@pytest.mark.base_table_methods
def test_postgresql_mysql_init():
    """
    Test __init__(**kwargs) method.
    """

    employees = Employees(emp_no=456000, birth_date='1954-04-30', first_name='Be Hai', \
                          last_name='Nguyen', gender='F', hire_date='2021-11-02')

    assert employees.emp_no == 456000
    assert employees.birth_date == '1954-04-30'
    assert employees.first_name == 'Be Hai'
    assert employees.last_name == 'Nguyen'
    assert employees.gender == 'F'
    assert employees.hire_date == '2021-11-02' 

@pytest.mark.base_table_methods
def test_postgresql_mysql_as_dict():
    employees = Employees(emp_no=456000, birth_date='1954-04-30', first_name='Be Hai', \
                          last_name='Nguyen', gender='F', hire_date='2021-11-02')
    
    employees_dict = employees.as_dict()

    assert employees_dict['emp_no'] == 456000
    assert employees_dict['birth_date'] == '1954-04-30'
    assert employees_dict['first_name'] == 'Be Hai'
    assert employees_dict['last_name'] == 'Nguyen'
    assert employees_dict['gender'] == 'F'
    assert employees_dict['hire_date'] == '2021-11-02' 

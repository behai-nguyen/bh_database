"""Test BaseModel (from core.py), and hence BaseTable, ReadOnlyTable, 
WriteCapableTable classes.

Tests for the def __str__(self) and the def __repr__(self) dunder methods.

These tests are database neutral and don't require a database connection.

To run only tests in this module: pytest -m base_table_dunder

To run all tests with PostgreSQL database: pytest -k _postgresql_ -v
To run all tests with MySQL database: pytest -k _mysql_ -v
"""

import pytest

from tests.employees import Employees

@pytest.mark.base_table_dunder
def test_postgresql_mysql_dunder_methods():
    employees = Employees()

    employees.emp_no = 456000
    employees.birth_date = '1954-04-30'
    employees.first_name = 'Be Hai'
    employees.last_name = 'Nguyen'
    employees.gender = 'F'
    employees.hire_date = '2021-11-02' 

    employees_str = ( "Employees: emp_no: 456000, birth_date: '1954-04-30', first_name: "
                     "'Be Hai', last_name: 'Nguyen', gender: 'F', hire_date: '2021-11-02'" )
    
    assert str(employees) == employees_str

    employees_repr = ("Employees(emp_no=456000, birth_date='1954-04-30', first_name='Be Hai', "
                      "last_name='Nguyen', gender='F', hire_date='2021-11-02')")

    assert repr(employees) == employees_repr

    employees1 = eval( employees_repr )
    assert employees1.emp_no == 456000
    assert employees1.birth_date == '1954-04-30'
    assert employees1.first_name == 'Be Hai'
    assert employees1.last_name == 'Nguyen'
    assert employees1.gender == 'F'
    assert employees1.hire_date == '2021-11-02' 

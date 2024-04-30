"""
Test EmployeesManager business component.

venv\Scripts\pytest.exe -m employees_mgr
venv\Scripts\pytest.exe -k _business_ -v

Use --capture=no to enable print output. I.e.:

venv\Scripts\pytest.exe -m employees_mgr --capture=no
"""

import pytest

from http import HTTPStatus

import datetime

from fastapir.business.employees_validation import (
    PARTIAL_LAST_NAME_MSG,
    PARTIAL_FIRST_NAME_MSG,
    BIRTH_DATE_MSG,
    LAST_NAME_MSG,
    FIRST_NAME_MSG,
    GENDER_MSG,
    HIRE_DATE_MSG,
    HIRE_DATE_AFTER_BIRTH_DATE_MSG,
)

from fastapir.business.employees_mgr import (
    EmployeesManager,
    ERR_INVALID_SEARCH_EMP_NUMBER_MSG
)

from tests import delete_employee

@pytest.mark.employees_mgr
def test_business_select_by_partial_last_name_and_first_name_invalid(app):
    """
    {
        "status": {
            "code": 500,
            "text": ""
        },
        "data": {
            "errors": [
                {
                    "id": "last_name",
                    "label": "Partial Last Name",
                    "errors": [
                        "Please provide partial search last name between 1 and 16 characters, must include wildcard %. E.g. %nas%"
                    ]
                },
                {
                    "id": "first_name",
                    "label": "Partial First Name",
                    "errors": [
                        "Please provide partial search first name between 1 and 14 characters, must include wildcard %. E.g. %An"
                    ]
                }
            ]
        }
    }
    """

    employees_mgr = EmployeesManager()

    status = employees_mgr.select_by_partial_last_name_and_first_name('', '')

    assert status.code == HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert hasattr(status, 'data') == True
    assert status.data != None
    assert hasattr(status.data, 'errors') == True
    assert len(status.data.errors) == 2

    error = status.data.errors[ 0 ]
    assert error[ 'id' ] == 'last_name'
    assert error[ 'label' ] == 'Partial Last Name'
    assert len(error[ 'errors' ]) == 1
    assert error[ 'errors' ][ 0 ] == PARTIAL_LAST_NAME_MSG

    error = status.data.errors[ 1 ]
    assert error[ 'id' ] == 'first_name'
    assert error[ 'label' ] == 'Partial First Name'
    assert len(error[ 'errors' ]) == 1
    assert error[ 'errors' ][ 0 ] == PARTIAL_FIRST_NAME_MSG

    status = employees_mgr.select_by_partial_last_name_and_first_name('nas', 'An')

    assert status.code == HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert hasattr(status, 'data') == True
    assert status.data != None
    assert hasattr(status.data, 'errors') == True
    assert len(status.data.errors) == 2

    error = status.data.errors[ 0 ]
    assert error[ 'id' ] == 'last_name'
    assert error[ 'label' ] == 'Partial Last Name'
    assert len(error[ 'errors' ]) == 1
    assert error[ 'errors' ][ 0 ] == PARTIAL_LAST_NAME_MSG

    error = status.data.errors[ 1 ]
    assert error[ 'id' ] == 'first_name'
    assert error[ 'label' ] == 'Partial First Name'
    assert len(error[ 'errors' ]) == 1
    assert error[ 'errors' ][ 0 ] == PARTIAL_FIRST_NAME_MSG

@pytest.mark.employees_mgr
def test_business_select_by_employee_number_invalid(app):
    employees = EmployeesManager()

    status = employees.select_by_employee_number(-10399)

    assert status.code == HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert status.text == ERR_INVALID_SEARCH_EMP_NUMBER_MSG
    assert status.data == None

@pytest.mark.employees_mgr
def test_business_select_by_partial_last_name_and_first_name(app):
    """
    Dates are not serialised!
    """
    employees_mgr = EmployeesManager()

    status = employees_mgr.select_by_partial_last_name_and_first_name('%nas%', '%An')

    assert status.code == HTTPStatus.OK.value
    assert len(status.text) > 0
    assert status.data != None
    assert len(status.data) >= 30

    assert status.data[0]['emp_no'] == 12483
    assert status.data[0]['birth_date'] == datetime.date(1959, 10, 19)
    assert status.data[0]['first_name'] == 'Niranjan'
    assert status.data[0]['last_name'] == 'Gornas'
    assert status.data[0]['gender'] == 'M'
    assert status.data[0]['hire_date'] == datetime.date(1990, 1, 10)

@pytest.mark.employees_mgr
def test_business_select_by_employee_number(app):
    """
    Dates are in Australian format.
    """

    employees = EmployeesManager()

    status = employees.select_by_employee_number(10399)

    assert status.code == HTTPStatus.OK.value
    assert len(status.text) > 0
    assert status.data != None
    assert len(status.data) == 1

    assert status.data[0]['emp_no'] == 10399
    assert status.data[0]['birth_date'] == '13/06/1957'
    assert status.data[0]['first_name'] == 'Guenter'
    assert status.data[0]['last_name'] == 'Marchegay'
    assert status.data[0]['gender'] == 'F'
    assert status.data[0]['hire_date'] == '07/05/1985'

    status_dict = status.as_dict()
    assert status_dict['status']['code'] == HTTPStatus.OK.value
    assert len( status_dict['status']['text'] ) > 0
    assert status_dict['data'][0]['emp_no'] == 10399
    assert status_dict['data'][0]['birth_date'] == '13/06/1957'
    assert status_dict['data'][0]['first_name'] == 'Guenter'
    assert status_dict['data'][0]['last_name'] == 'Marchegay'
    assert status_dict['data'][0]['gender'] == 'F'
    assert status_dict['data'][0]['hire_date'] == '07/05/1985'

@pytest.mark.employees_mgr
def test_business_write_employee_invalid(app):
    try:
        delete_employee('Do%', 'Be %')

        employee = {}
        # This is a new record, we don't have to specify None for primary key.
        employee['empNo'] = None
        employee['birthDate'] = ''
        employee['firstName'] = ''
        employee['lastName'] = ''
        employee['gender'] = ''
        employee['hireDate'] = ''

        status = EmployeesManager().write_to_database(employee)

        # print("\nstatus.as_dict(): ", status.as_dict(), "\n")

        assert status.code == HTTPStatus.INTERNAL_SERVER_ERROR.value
        assert hasattr(status, 'data') == True
        assert status.data != None
        assert hasattr(status.data, 'errors') == True
        assert len(status.data.errors) == 5

        error = status.data.errors[ 0 ]
        assert error[ 'id' ] == 'birth_date'
        assert error[ 'label' ] == 'Birth Date'
        assert len(error[ 'errors' ]) == 1
        assert error[ 'errors' ][ 0 ] == BIRTH_DATE_MSG

        error = status.data.errors[ 1 ]
        assert error[ 'errors' ][ 0 ] == FIRST_NAME_MSG

        error = status.data.errors[ 2 ]
        assert error[ 'errors' ][ 0 ] == LAST_NAME_MSG

        error = status.data.errors[ 3 ]
        assert error[ 'errors' ][ 0 ] == GENDER_MSG

        error = status.data.errors[ 4 ]
        assert error[ 'errors' ][ 0 ] == HIRE_DATE_MSG

        employee = {}
        # This is a new record, we don't have to specify None for primary key.
        # employee['empNo'] = None
        employee['birthDate'] = '25/12/1971'
        employee['firstName'] = 'Be Hai'
        employee['lastName'] = 'Doe'
        employee['gender'] = 'M'
        # Note: there is no leading 0 in single digit day, month.
        employee['hireDate'] = '17/9/1967'

        status = EmployeesManager().write_to_database(employee)

        # print("\nstatus.as_dict(): ", status.as_dict(), "\n")

        assert status.code == HTTPStatus.INTERNAL_SERVER_ERROR.value
        assert hasattr(status, 'data') == True
        assert status.data != None
        assert hasattr(status.data, 'errors') == True
        assert len(status.data.errors) == 1

        error = status.data.errors[ 0 ]
        assert error[ 'id' ] == 'hire_date'
        assert error[ 'label' ] == 'Hire Date'
        assert len(error[ 'errors' ]) == 1
        assert error[ 'errors' ][ 0 ] == HIRE_DATE_AFTER_BIRTH_DATE_MSG
    finally:
        delete_employee('Do%', 'Be %')

@pytest.mark.employees_mgr
def test_business_write_employee(app):
    try:
        delete_employee('Do%', 'Be %')

        """
        Insert a new employee.
        """
        employee = {}
        # This is a new record, we don't have to specify None for primary key.
        # employee['empNo'] = None
        employee['birthDate'] = '25/12/1971'
        employee['firstName'] = 'Be Hai'
        employee['lastName'] = 'Doe'
        employee['gender'] = 'M'
        # Started working at around 4 years and 3 months old!!!
        # Note: there is no leading 0 in single digit day, month.
        employee['hireDate'] = '17/9/1975'

        status = EmployeesManager().write_to_database(employee)

        # print("\nstatus.as_dict(): ", status.as_dict(), "\n")

        assert status.code == HTTPStatus.OK.value
        assert status.data != None
        assert hasattr(status.data, 'employees_new_list') == True
        assert hasattr(status.data, 'employees_updated_list') == True
        
        # There is one (1) new record.
        # There is no updated record.
        assert len(status.data.employees_new_list) == 1
        assert len(status.data.employees_updated_list) == 0

        new_emp_no = status.data.employees_new_list[0]['emp_no']
        # 499999 is the last emp_no in the original test data.
        assert new_emp_no > 499999

        """
        Read the newly inserted employee back and verify data inserted.
        """
        status = EmployeesManager().select_by_employee_number(new_emp_no)
        
        assert status.code == HTTPStatus.OK.value
        assert status.data != None
        assert len(status.data) == 1

        assert status.data[0]['emp_no'] == new_emp_no
        assert status.data[0]['birth_date'] == '25/12/1971'
        assert status.data[0]['first_name'] == 'Be Hai'
        assert status.data[0]['last_name'] == 'Doe'
        assert status.data[0]['gender'] == 'M'
        # Note: THERE IS LEADING 0 in single digit day, month.
        assert status.data[0]['hire_date'] == '17/09/1975'

        """
        Update the just inserted employee:
            - set Gender to F
            - set Hire Date to 11/8/2005
        """
        employee['empNo'] = new_emp_no
        employee['gender'] = 'F'
        employee['hireDate'] = '11/8/2005'

        status = EmployeesManager().write_to_database(employee)

        assert status.code == HTTPStatus.OK.value
        assert status.data != None
        assert hasattr(status.data, 'employees_new_list') == True
        assert hasattr(status.data, 'employees_updated_list') == True
        
        # There is no new record.
        # There is one (1) updated record.
        assert len(status.data.employees_new_list) == 0
        assert len(status.data.employees_updated_list) == 1

        """
        Read the newly updated employee back and verify data updated.
        """
        status = EmployeesManager().select_by_employee_number(new_emp_no)
        
        assert status.code == HTTPStatus.OK.value
        assert status.data != None
        assert len(status.data) == 1

        assert status.data[0]['emp_no'] == new_emp_no
        assert status.data[0]['birth_date'] == '25/12/1971'
        assert status.data[0]['first_name'] == 'Be Hai'
        assert status.data[0]['last_name'] == 'Doe'
        assert status.data[0]['gender'] == 'F'
        assert status.data[0]['hire_date'] == '11/08/2005'

    finally:
        delete_employee('Do%', 'Be %')

"""
Test Employees model: i.e. "employees" table.

venv\Scripts\pytest.exe -m employees
venv\Scripts\pytest.exe -k _unit_ -v

Use --capture=no to enable print output. I.e.:

venv\Scripts\pytest.exe -m employees --capture=no
"""

import pytest

from http import HTTPStatus

import datetime

from flaskr.models.employees import Employees

@pytest.mark.employees
def test_unit_select_by_partial_last_name_and_first_name(app):
    """
    Dates are not serialised!
    """
    employees = Employees()

    status = employees.select_by_partial_last_name_and_first_name('%nas%', '%An')

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

@pytest.mark.employees
def test_unit_select_by_employee_number(app):
    """
    Dates are in Australian format.
    """
    employees = Employees()

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

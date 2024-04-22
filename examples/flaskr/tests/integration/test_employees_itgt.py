"""
Test Employees related routes.

We have only valid tests. Respectively, these are the equivalent of 
the following two Business tests:

    @pytest.mark.employees_mgr
    def test_business_select_by_partial_last_name_and_first_name(app):

    @pytest.mark.employees_mgr
    def test_business_write_employee(app):

Invalid tests should only be involving submitting invalid data, and
tests for failed response.

venv\Scripts\pytest.exe -m employees_integration
venv\Scripts\pytest.exe -k _integration_ -v

Use --capture=no to enable print output. I.e.:

venv\Scripts\pytest.exe -m employees_integration --capture=no
"""
import pytest

from http import HTTPStatus

import simplejson as json

from tests import delete_employee

@pytest.mark.employees_integration
def test_integration_select_by_partial_last_name_and_first_name(test_client):
    """
    Test search employee.
    """
    response = test_client.post('/employees/search/%nas%/%An')

    assert response != None
    assert response.status_code == HTTPStatus.OK.value

    html = response.get_data(as_text=True)

    assert html.find('<!DOCTYPE html>') > -1

    i1 = html.find(' data-item-id="12483" ')
    assert i1 > -1
    i2 = html.find('<div class="col-3">Niranjan</div>') 
    assert i2 > -1
    assert (i2 > i1) == True

    assert html.find('<div class="col-3">Gopalakrishnan</div>') > -1

@pytest.mark.employees_integration
def test_integration_write_employee(test_client):
    """
    Test write employee to database.
    """
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

        response = test_client.post('/employees/save', data=employee)
        assert response != None
        assert response.status_code == HTTPStatus.OK.value

        status = json.loads(response.get_data(as_text=True))

        # print("\nstatus: ", status, "\n")

        assert status['status']['code'] == HTTPStatus.OK.value
        assert status['data'] != None
        assert ('employees_new_list' in status['data']) == True
        assert ('employees_updated_list' in status['data']) == True
        
        # There is one (1) new record.
        employees_new_list = status['data']['employees_new_list']
        # There is no updated record.
        employees_updated_list = status['data']['employees_updated_list']
        assert len(employees_new_list) == 1
        assert len(employees_updated_list) == 0

        new_emp_no = employees_new_list[0]['emp_no']
        # 499999 is the last emp_no in the original test data.
        assert new_emp_no > 499999

        """
        Read the newly inserted employee back and verify data inserted.
        """
        response = test_client.get(f'/employees/search-by-emp-no/{new_emp_no}')
        status = json.loads(response.get_data(as_text=True))
        
        assert status['status']['code'] == HTTPStatus.OK.value
        assert status['data'] != None
        data = status['data']
        assert len(data) == 1

        assert data[0]['emp_no'] == new_emp_no
        assert data[0]['birth_date'] == '25/12/1971'
        assert data[0]['first_name'] == 'Be Hai'
        assert data[0]['last_name'] == 'Doe'
        assert data[0]['gender'] == 'M'
        # Note: THERE IS LEADING 0 in single digit day, month.
        assert data[0]['hire_date'] == '17/09/1975'

        """
        Update the just inserted employee:
            - set Gender to F
            - set Hire Date to 11/8/2005
        """
        employee['empNo'] = new_emp_no
        employee['gender'] = 'F'
        employee['hireDate'] = '11/8/2005'

        response = test_client.post('/employees/save', data=employee)

        assert response != None
        assert response.status_code == HTTPStatus.OK.value

        status = json.loads(response.get_data(as_text=True))

        assert status['status']['code'] == HTTPStatus.OK.value
        assert status['data'] != None
        assert ('employees_new_list' in status['data']) == True
        assert ('employees_updated_list' in status['data']) == True

        # There is no new record.
        employees_new_list = status['data']['employees_new_list']
        # There is one (1) updated record.
        employees_updated_list = status['data']['employees_updated_list']
        assert len(employees_new_list) == 0
        assert len(employees_updated_list) == 1

        """
        Read the newly updated employee back and verify data updated.
        """
        response = test_client.get(f'/employees/search-by-emp-no/{new_emp_no}')
        status = json.loads(response.get_data(as_text=True))
        
        assert status['status']['code'] == HTTPStatus.OK.value
        assert status['data'] != None
        data = status['data']
        assert len(data) == 1

        assert data[0]['emp_no'] == new_emp_no
        assert data[0]['birth_date'] == '25/12/1971'
        assert data[0]['first_name'] == 'Be Hai'
        assert data[0]['last_name'] == 'Doe'
        assert data[0]['gender'] == 'F'
        assert data[0]['hire_date'] == '11/08/2005'

    finally:
        delete_employee('Do%', 'Be %')

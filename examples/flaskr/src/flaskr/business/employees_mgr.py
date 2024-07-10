"""
Business components should be (web) framework neutral.

Employees implementations: validating submitted data, managing CRUD on 
validated data, etc.
"""

import logging
from http import HTTPStatus

from bh_apistatus.result_status import (
    ResultStatus,
    make_500_status,
    clone_status,
)

from bh_database.constant import BH_REC_STATUS_FIELDNAME

from bh_utils.date_funcs import australian_date_to_iso_datetime

from .app_business import AppBusiness

from .base_validation import validate
from .employees_validation import (
    SearchByNameForm,
    EditorForm,
)

from flaskr.models.employees import Employees

ERR_INVALID_SEARCH_EMP_NUMBER_MSG = 'Invalid search employee number.'

logger = logging.getLogger('flaskr.example')

class EmployeesManager(AppBusiness):
    """    
    Validate submitted data.
    Carry out CRUD operations on Employees table.

    self.__employee_data: data dictionary which presents an employee 
        record, read to be written into database.
    """

    def __init__(self):
        super().__init__()
        self.__employee_data = None

    """
    Add any required decorator as required. E.g.:

    @login_required

    To keep the example simple, we don't implement any decorator.
    """
    def select_by_partial_last_name_and_first_name(self, 
            last_name: str, first_name: str) -> ResultStatus:
        try:
            search_data = {'last_name': last_name, 'first_name': first_name}
            status = validate(search_data, [SearchByNameForm])
            if (status.code != HTTPStatus.OK.value): return status

            return Employees().select_by_partial_last_name_and_first_name(
                last_name, first_name)

        except Exception as e:
            logger.exception(str(e))
            return make_500_status(str(e))
        
    """
    Add any required decorator as required. E.g.:

    @login_required

    To keep the example simple, we don't implement any decorator.
    """
    def select_by_employee_number(self, emp_no: int) -> ResultStatus:
        try:
            # 10001 is from the database.
            if emp_no < 10001:
                return make_500_status(ERR_INVALID_SEARCH_EMP_NUMBER_MSG)

            return Employees().select_by_employee_number(emp_no)

        except Exception as e:
            logger.exception(str(e))
            return make_500_status(str(e))
        
    """
    Write to database methods.
    """
        
    def _preprocess_write_data(self):
        """ Override. 
        
        Prepares self.__employee_data, a proper employee dictionary 
        from the submitted data stored in self._write_data. The data 
        in self.__employee_data gets written to the database.

        Return:

        A ready-to-write dictionary which represents a single employee.        
        """

        self.__employee_data = {}
        self._param_to_record(self.__employee_data, 'empNo', 'emp_no')
        self._param_to_record(self.__employee_data, 'birthDate', 'birth_date')
        self._param_to_record(self.__employee_data, 'firstName', 'first_name')
        self._param_to_record(self.__employee_data, 'lastName', 'last_name')
        self._param_to_record(self.__employee_data, 'gender', 'gender')
        self._param_to_record(self.__employee_data, 'hireDate', 'hire_date')
        # This field indicates whether this is an updated employee or a new 
        # employee.
        self.__employee_data[BH_REC_STATUS_FIELDNAME] = self._get_rec_status('empNo')

        return super()._preprocess_write_data()

    def _validate(self):
        """ Override. """

        # Note: 'birth_date' and 'hire_date' are in Australian 
        # date format. That is, dd/mm/yyyy.
        return validate(self.__employee_data, [EditorForm])

    def _pre_write(self):        
        """ Override. """

        # Australian date to MySQL date.
        self.__employee_data['birth_date'] = australian_date_to_iso_datetime(self.__employee_data['birth_date'], False)
        self.__employee_data['hire_date'] = australian_date_to_iso_datetime(self.__employee_data['hire_date'], False)

        return super()._pre_write()

    def _write(self):
        """ Override. 
        
        Return:
            On failure:
            {
                "status": {
                    "code": 500,
                    "text": "blah..."
                }
            }

            On successful:
            {
                "status": {
                    "code": 200,
                    "text": "Data has been saved successfully."
                },
                "data": {
                    "employees_new_list": [
                        {
                            "emp_no": 500218,
                            "birth_date": "1973-04-03",
                            "first_name": "Be Hai",
                            "last_name": "Doe",
                            "gender": "M",
                            "hire_date": "2024-04-12"
                        }
                    ],
                    "employees_updated_list": []
                }
            }

            - "employees_new_list" is populated if the written record was new.
            - ""employees_updated_list" is populated if the written record was updated.
        """

        logger.debug('Entered...')
        try:
            employee = Employees()

            employee.begin_transaction()

            # raise Exception('Test Exception...')

            status = employee.write_to_database([self.__employee_data])

            # Failed to write to {employee.__tablename__} table.
            if status.code != HTTPStatus.OK.value:
                self._write_last_result = status
                return

            # Successful.
            self._write_last_result = clone_status(status)

            # Attach two data fields "employees_new_list" and "employees_updated_list" 
            # to the return write result. These are single element lists. And one of
            # the two would empty.
            data_name = f"{employee.__tablename__}_new_list"
            self._write_last_result.add_data(getattr(status.data, data_name), data_name)

            data_name = f"{employee.__tablename__}_updated_list"
            self._write_last_result.add_data(getattr(status.data, data_name), data_name)

        except Exception as e:
            logger.exception(str(e))
            self._write_last_result = make_500_status(str(e))

        finally:
            employee.finalise_transaction(self._write_last_result)
            logger.debug('Exited.')
            return self._write_last_result

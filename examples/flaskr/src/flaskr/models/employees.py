"""
Employees model.
"""

from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
)

from bh_apistatus.result_status import ResultStatus

from bh_database.base_table import WriteCapableTable

class Employees(WriteCapableTable):
    __tablename__ = 'employees'

    emp_no = Column(Integer, primary_key=True)
    birth_date = Column(Date, nullable=False)
    first_name = Column(String(14), nullable=False)
    last_name = Column(String(16), nullable=False)
    gender = Column(String(1), nullable=False)
    hire_date = Column(Date, nullable=False)

    def select_by_partial_last_name_and_first_name(self, 
            last_name: str, first_name: str) -> ResultStatus:
        
        return self.run_stored_proc('get_employees', [last_name, first_name], True)

    def select_by_employee_number(self, emp_no: int) -> ResultStatus:
        return self.run_select_sql(
            'select * from employees where emp_no = {0}'.format(emp_no), True)

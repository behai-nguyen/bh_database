"""
Employees test model and associated test constants and methods.
"""
from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
)

from bh_database.base_table import WriteCapableTable

class Employees(WriteCapableTable):
    __tablename__ = 'employees'

    emp_no = Column(Integer, primary_key=True)
    birth_date = Column(Date, nullable=False)
    first_name = Column(String(14), nullable=False)
    last_name = Column(String(16), nullable=False)
    gender = Column(String(1), nullable=False)
    hire_date = Column(Date, nullable=False)

SELECT_EMPLOYEES = ("select * from employees where (upper(last_name) like '%NAS%')" 
    " and (upper(first_name) like '%AN') order by emp_no;")

def assert_employees_list_of_tuples(rows: list) -> None:
    assert rows[0][2] == 'Niranjan'
    assert rows[0][3] == 'Gornas'

    assert rows[len(rows)-1][2] == 'Gopalakrishnan'
    assert rows[len(rows)-1][3] == 'Gornas'

def assert_employees_list_of_dicts(rows: list) -> None:
    assert rows[0]['first_name'] == 'Niranjan'
    assert rows[0]['last_name'] == 'Gornas'

    assert rows[len(rows)-1]['first_name'] == 'Gopalakrishnan'
    assert rows[len(rows)-1]['last_name'] == 'Gornas'

"""Test the paginating functionality of BaseQuery class with MySQL database.

To run only tests in this module: pytest -m paginator_mysql

To run all tests with MySQL database: pytest -k _mysql_ -v

On mysql() fixture:
-------------------

To ensure each test module can run independently and does not inadvertently produce
any side effects on later tests, or tests in other modules, the mysql() fixture needs 
to be called only once for this module.

The mysql() fixture establishes a connection to the underlying MySQL Employees Sample 
Database. This call is similar to applications establish database connection on starting up.
"""

import pytest

from bh_database import core

from tests.employees import Employees

@pytest.mark.paginator_mysql
def test_mysql_prepare(mysql):
    """Database connection management.

    The purpose of this method is to establish the connection to the database.
    The mysql() method need to run FIRST and ONCE to establish the connection.

    I find this sort of work around is the most reliable method to control codes
    execution sequence.
    """

    assert core.BaseSQLAlchemy.session != None
    # BaseSQLAlchemy is abstract, with no table name.
    assert core.BaseSQLAlchemy.query == None

    assert Employees.query != None

@pytest.mark.paginator_mysql
def test_mysql_paginator_01():
    """
    First page.
    """
    paginator = Employees.query.filter(Employees.last_name.ilike('%NAS%')).\
        order_by(Employees.emp_no).paginate(page=1, per_page=10)

    assert paginator != None

    assert paginator.total_records == 573
    assert paginator.total_pages == 58
    assert len(paginator.items) == 10

    assert paginator.page == 1
    assert paginator.per_page == 10
    assert paginator.offset == 0 # page 1
    assert paginator.limit == 10
    assert paginator.has_next == True
    assert paginator.has_prev == False

    employee = paginator.items[0].as_dict()
    assert employee['emp_no'] == 10155
    assert employee['first_name'] == 'Adas'
    assert employee['last_name'] == 'Nastansky'

    employee = paginator.items[9].as_dict()
    assert employee['emp_no'] == 15174
    assert employee['first_name'] == 'Otilia'
    assert employee['last_name'] == 'Salinas'

@pytest.mark.paginator_mysql
def test_mysql_paginator_02():
    """
    Last page.
    """
    paginator = Employees.query.filter(Employees.last_name.ilike('%NAS%')).\
        order_by(Employees.emp_no).paginate(page=58, per_page=10)

    assert paginator != None

    assert paginator.total_records == 573
    assert paginator.total_pages == 58
    assert len(paginator.items) == 3

    assert paginator.page == 58
    assert paginator.per_page == 10
    assert paginator.offset == 570 # page (58 - 1)*10
    assert paginator.limit == 10
    assert paginator.has_next == False
    assert paginator.has_prev == True

    employee = paginator.items[0].as_dict()
    assert employee['emp_no'] == 498483
    assert employee['first_name'] == 'Sivanarayana'
    assert employee['last_name'] == 'Gornas'

    employee = paginator.items[2].as_dict()
    assert employee['emp_no'] == 499704
    assert employee['first_name'] == 'Luisa'
    assert employee['last_name'] == 'Nastansky'
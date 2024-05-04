Getting Started -- Please Read First
====================================

Database classes using SQLAlchemy.

Required drivers 
----------------

These classes currently support only two database types: MySQL and PostgreSQL. Drivers 
required for MySQL and PostgreSQL, respectively:

    * `https://pypi.org/project/mysql-connector-python/ <https://pypi.org/project/mysql-connector-python/>`_.
    * `https://pypi.org/project/psycopg2/ <https://pypi.org/project/psycopg2/>`_.

This package installs both drivers, remove the one not required.

:To remove MySQL driver:

    pip uninstall mysql-connector-python

:To remove PostgreSQL driver:

    pip uninstall psycopg2

.. _getting-started-database-requirements:

Database requirements
---------------------

This package **assumes** that primary keys for tables are of type integer. And each table 
only has a single primary integer key.

It requires the target database to implement ``unique_id`` table and associated ``get_unique_id`` 
stored method. Scripts to create these can be found under the 
`repo ./sql_scripts sub-directory <https://github.com/behai-nguyen/bh_database/tree/main/sql_scripts>`_:

:MySQL:

    * `./sql_scripts/mysql/01_unique_id_table.sql <https://github.com/behai-nguyen/bh_database/blob/main/sql_scripts/mysql/01_unique_id_table.sql>`_.
    * `./sql_scripts/mysql/02_get_unique_id_stored_method.sql <https://github.com/behai-nguyen/bh_database/blob/main/sql_scripts/mysql/02_get_unique_id_stored_method.sql>`_.

:PostgreSQL:

    * `./sql_scripts/postgres/01_unique_id_table.sql <https://github.com/behai-nguyen/bh_database/blob/main/sql_scripts/postgres/01_unique_id_table.sql>`_.
    * `./sql_scripts/postgres/02_get_unique_id_stored_method.sql <https://github.com/behai-nguyen/bh_database/blob/main/sql_scripts/postgres/02_get_unique_id_stored_method.sql>`_.

The test database
-----------------

The test database is the MySQL *Employees Sample Database*, recommended (*) by 
Oracle Corporation, downloadable from `https://github.com/datacharmer/test_db <https://github.com/datacharmer/test_db>`_.

(*) The official documentation page `Employees Sample Database <https://dev.mysql.com/doc/employee/en/>`_.

This MySQL database has been migrated to PostgreSQL as described in 
`pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL.
<https://behainguyen.wordpress.com/2022/11/13/pgloader-docker-migrating-from-docker-localhost-mysql-to-localhost-postgresql/>`_

In addition to the two (2) required SQL scripts mentioned in :ref:`getting-started-database-requirements`, 
the two (2) below must be applied to *Employees Sample Database*, these are required to run the 
tests in this package.

:MySQL:

    * `./sql_scripts/mysql/03_test_employees_preparation.sql <https://github.com/behai-nguyen/bh_database/blob/main/sql_scripts/mysql/03_test_employees_preparation.sql>`_.
    * `./sql_scripts/mysql/04_test_get_employees_stored_method.sql <https://github.com/behai-nguyen/bh_database/blob/main/sql_scripts/mysql/04_test_get_employees_stored_method.sql>`_.

:PostgreSQL:

    * `./sql_scripts/postgres/03_test_employees_preparation.sql <https://github.com/behai-nguyen/bh_database/blob/main/sql_scripts/postgres/03_test_employees_preparation.sql>`_.
    * `./sql_scripts/postgres/04_test_get_employees_stored_method.sql <https://github.com/behai-nguyen/bh_database/blob/main/sql_scripts/postgres/04_test_get_employees_stored_method.sql>`_.

Running the tests
-----------------

Tests have been grouped for each database type. They are identical tests, except for 
the initial database connection at the beginning of each test module.

:To run tests for MySQL:

    pytest -k _mysql_ -v

:To run tests for PostgreSQL:

    pytest -k _postgresql_ -v

:To run a specific test: pytest -m <marker> (markers are defined in ``pytest.ini``).

Test modules
------------

There are following core modules:

.. line-block::
   
    ./tests/test_01_core_database_postgresql.py
    ./tests/test_02_core_database_mysql.py
    ./tests/test_05_core_basesqlalchemy_postgresql.py
    ./tests/test_06_core_basesqlalchemy_mysql.py
    ./tests/test_11_paginator_postgresql.py
    ./tests/test_12_paginator_mysql.py
    ./tests/test_15_base_table_postgresql.py
    ./tests/test_16_base_table_mysql.py
    ./tests/test_17_base_table_methods.py
    ./tests/test_20_base_table_dunder.py

These test modules, together with fixtures defined in ``./tests/conftest.py``
should illustrate how the classes in this core module should work together.

The following model (table) oriented modules demonstrate how applications should 
subclass and use the methods in place to do database works:

.. line-block::

    ./tests/test_25_base_table_crud_methods_postgresql.py
    ./tests/test_26_base_table_crud_methods_mysql.py
    ./tests/test_30_base_table_exception_postgresql.py
    ./tests/test_31_base_table_exception_mysql.py
Installation
============

This package currently supports only two database types: MySQL and PostgreSQL. The drivers 
required for MySQL and PostgreSQL are as follows:

    * For MySQL: `https://pypi.org/project/mysql-connector-python/ <https://pypi.org/project/mysql-connector-python/>`_.
    * For PostgreSQL: `https://pypi.org/project/psycopg2/ <https://pypi.org/project/psycopg2/>`_.

By default, this package does not install either of the above two drivers. They must 
be installed explicitly.

To install for MySQL using the `mysql-connector-python <https://pypi.org/project/mysql-connector-python>`_ 
driver, use the following command::

    pip install bh-database[mysql-connector-python]

To install for PostgreSQL using the `psycopg2 <https://pypi.org/project/psycopg2>`_ driver, 
use the following command::

    pip install bh-database[psycopg2-binary]

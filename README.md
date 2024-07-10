# bh_database

Database wrapper classes for SQLAlchemy.

## Installation

To install for MySQL using the [mysql-connector-python](https://pypi.org/project/mysql-connector-python) driver, use the following command:

```
pip install bh-database[mysql-connector-python]
```

To install for PostgreSQL using the [psycopg2](https://pypi.org/project/psycopg2) driver, 
use the following command::

```
pip install bh-database[psycopg2-binary]
```

## Overview

Database wrapper classes for SQLAlchemy.

These classes currently support only two database types: MySQL and PostgreSQL. Drivers 
required, respectively:

* [https://pypi.org/project/mysql-connector-python](https://pypi.org/project/mysql-connector-python/).
* [https://pypi.org/project/psycopg2/](https://pypi.org/project/psycopg2/).
    
These classes provide the following functionalities:

* Database connection management.

* A custom SQLAlchemy query class which implements paginating.

* A generic base model (table), which should be the **indirect** base model for 
    applications' models. This class encapsulates:
        
    * SQLAlchemy scoped session, thereby providing methods to implement transaction atomicity.

    * A custom base query with paginating ability mentioned above.

    * Fully implemented dunder methods str() and repr().

* A generic SQLAlchemy declarative base class which should include all required metaclasses.

* Some generic methods which run full text SQL statements.

* A generic method to run stored procedures which return data.

* A generic method which takes a list of records to be inserted, and records to be
    updated, and writes them to the target database table in a single call.

* Transaction atomicity. Multiple database operations involving several different
    tables can be wrapped under a single transaction, so that all can be committed
    or rolled back as appropriate. 

Please see [Full documentation](https://bh-database.readthedocs.io/) for more detail.

## Documentation

[Full documentation](https://bh-database.readthedocs.io/)

## License

[ MIT license ](http://www.opensource.org/licenses/mit-license.php)
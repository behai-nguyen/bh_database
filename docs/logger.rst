Application Logger Configuration
--------------------------------

This package uses the default ``bh_database`` logger. This logger is set with a `‘no-op’ NullHandler 
handler <https://docs.python.org/3/library/logging.handlers.html#logging.NullHandler>`_, 
as recommended by the official documentation on 
`Configuring Logging for a Library <https://docs.python.org/3/howto/logging.html#library-config>`_ .

This package also includes the `bh-utils <https://bh-utils.readthedocs.io/en/latest/index.html>`_ 
package. Although none of the functions called from ``bh-utils`` perform any logging, the 
``bh-utils`` logging configuration is implemented in the following example for the sake of 
completeness and illustrative purposes.

The following example demonstrates how applications can enable this logger.

**The logging.yaml logger configuration:**

.. code-block:: yaml

    version: 1
    disable_existing_loggers: False
    formatters:
        default:
            format: '%(levelname)s [%(asctime)s] %(thread)s %(filename)s %(funcName)s %(lineno)s %(message)s'
            datefmt: '%d-%m-%Y %H:%M:%S'
    handlers:
        console:
            formatter: default
            class: logging.StreamHandler
            stream: ext://sys.stdout
    loggers:
        bh_database:
            level: DEBUG
            handlers:
                - console
            propagate: no
        bh_utils:
            level: DEBUG
            handlers:
                - console
            propagate: no
    root:
        level: INFO
        handlers:
            - console

**The demo.py Python script:**

.. code-block:: python

    import logging.config
    import yaml

    from sqlalchemy import (
        Column,
        Integer,
        Date,
        String,
    )

    from bh_database.core import Database
    from bh_database.base_table import WriteCapableTable

    from bh_apistatus.result_status import ResultStatus

    SQLALCHEMY_DATABASE_SCHEMA = 'employees'

    # Enable this for MySQL.
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:pcb.2176310315865259@localhost:3306/employees'

    # Enable this for PostgreSQL.
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:pcb.2176310315865259@localhost/employees'

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

    def register_loggers():
        with open('logger_config.yaml', 'rt') as file:
            config = yaml.safe_load(file.read())
            logging.config.dictConfig(config)

    register_loggers()

    Database.disconnect()
    Database.connect(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_DATABASE_SCHEMA)

    emp = Employees()

    status = emp.select_by_partial_last_name_and_first_name('%nas%', '%An')

    # print(status.as_dict())
    print(f"{len(status.data)} records matched the search criteria.")

**The command to run**::

    ▶️Windows 10: (venv) F:\\pydev>venv\\Scripts\\python.exe demo.py
    ▶️Ubuntu 22.10: (venv) behai@hp-pavilion-15:~/pydev$ ./venv/bin/python demo.py

**The output we should see**::

    (venv) behai@hp-pavilion-15:~/test$ ./venv/bin/python example.py
    DEBUG [09-07-2024 11:17:15] 139907046815552 base_table.py run_stored_proc 407 Entered
    DEBUG [09-07-2024 11:17:15] 139907046815552 base_table.py run_stored_proc 456 Exited.
    38 records matched the search criteria.
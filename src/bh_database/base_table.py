"""Implement some more abstract base model (table) classes.

These classes add some more generic database functionalities:

    * Some generic methods which run full text SQL statements.
    * A generic method to run stored procedures which return data.
    * A generic method which takes a list of records to be inserted, and records to be \
        updated, and writes them to the target database table in a single call.
    * Transaction atomicity. Multiple database operations involving several different \
        tables can be wrapped under a single transaction, so that all can be committed \
        or rolled back as appropriate. 

Applications should subclass their own tables from either one of these two 
classes :py:class:`ReadOnlyTable` and :py:class:`WriteCapableTable`.

Please note, :py:class:`WriteCapableTable` requires the target database to implement ``unique_id`` 
table and associated ``get_unique_id`` stored method, please see :ref:`getting-started-database-requirements`
for more detail.

Relevant test modules:

    * ./tests/test_25_base_table_crud_methods_postgresql.py
    * ./tests/test_26_base_table_crud_methods_mysql.py
    * ./tests/test_30_base_table_exception_postgresql.py
    * ./tests/test_31_base_table_exception_mysql.py
"""

from http import HTTPStatus
from contextlib import closing

from sqlalchemy import text

from sqlalchemy import (
    inspect,
    update,
)

import simplejson as json

from bh_utils import json_funcs
from bh_utils.conversions import is_integer

from bh_apistatus.result_status import (
    ResultStatus,
    make_status,
    make_500_status,
)

from bh_database.core import(
    Database,
    DatabaseType,
    BaseSQLAlchemy,
)

from bh_database.constant import (
    BH_UNSUPPORTED_DATABASE_MSG,
    BH_REC_STATUS_FIELDNAME,
    BH_RECORD_STATUS_NEW,
    BH_RECORD_STATUS_MODIFIED,
    BH_NEXT_ID_NO_RESULT_MSG,
    BH_STORED_PROC_NO_RESULT_SET_MSG,
    BH_SQL_NO_DATA_MSG,
    BH_RETRIEVED_SUCCESSFUL_MSG,
    BH_SAVED_SUCCESSFUL_MSG,
)

from bh_database import logger

class BaseTable(BaseSQLAlchemy):
    """An abstract base model (table).

    :param kwargs: column name, value pairs.

    For example::

        employees = Employees(emp_no=456000, ..., hire_date='2021-11-02')

    in::    
        
        class Employees(WriteCapableTable):
            emp_no = Column(Integer, primary_key=True)
            ...
            hire_date = Column(Date, nullable=False)

        employees = Employees(emp_no=456000, ..., hire_date='2021-11-02')

        assert employees.emp_no == 456000
        ...
        assert employees.hire_date == '2021-11-02' 

    where :py:class:`WriteCapableTable` is an indirect subclass of :py:class:`BaseTable`.

    In general, for this abstract class and its abstract descendant classes, do not 
    access :attr:`~bh_database.core.BaseSQLAlchemy.query` when not assigned. E.g.::

        assert BaseTable.query == None

    It results in the following exception::

        ArgumentError("Column expression, FROM clause, or other columns clause element expected, <class 'bh_database.core.BaseSQLAlchemy'>.")

    A relevant test module ``./tests/test_17_base_table_methods.py``.
    """
    __abstract__ = True

    def __get_primary_keys(self) -> list:
        """Collect primary key column names and return all as a list.

        Most tables have only a single primary key.

        Reference:
            https://stackoverflow.com/questions/25932166/generic-way-to-get-primary-key-from-declaratively-defined-instance-in-sqlalchemy
            Generic way to get primary key from declaratively defined instance in SQLAlchemy

        :return: a list of model primary keys.
        :rtype: list.
        """
        res = []
        ins_obj = inspect(type(self))

        for item in ins_obj.primary_key:
            res.append(item.key)

        return res

    def __init__(self, **kwargs):
        self._primary_keys = self.__get_primary_keys()
        self._primary_key = self._primary_keys[0]

        self._type = type(self)

        """Reference:      
            https://splunktool.com/how-can-you-set-class-attributes-from-variable-arguments-kwargs-in-python
            How can you set class attributes from variable arguments (kwargs) in python
        """
        self.__dict__.update(kwargs)

    def as_dict(self) -> dict:
        """Convert all column-value pairs of model instance to a dictionary.

        For a full example usage, please see test module ``./tests/test_17_base_table_methods.py``.

        :References:
            
            * `How to serialize SqlAlchemy result to JSON? \
                <https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json>`_
            
            * `How to convert SQLAlchemy row object to a Python dict? \
                <https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict>`_

        :return: all column-value pairs as a dictionary.
        :rtype: dict.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ReadOnlyTable(BaseTable):
    """Implement a *read-only* abstract base model (table) class.

    This table class should be the parent class for lookup tables, whom the contents 
    seldom change.

    *Read-only* in the sense that this class has only a public method to query database. 
    It is only a semantic classification. It is also an indirect child of 
    :py:class:`~bh_database.core.BaseSQLAlchemy` class, it can use class attributes
    :attr:`~bh_database.core.BaseSQLAlchemy.session` and 
    :attr:`~bh_database.core.BaseSQLAlchemy.query` to alter data directly.

    In general, for this abstract class and its abstract descendant classes, do not 
    access :attr:`~bh_database.core.BaseSQLAlchemy.query` when not assigned. E.g.::

        assert ReadOnlyTable.query == None

    It results in the following exception::

        ArgumentError("Column expression, FROM clause, or other columns clause element expected, <class 'bh_database.core.BaseSQLAlchemy'>.")
    """
    
    __abstract__ = True

    def run_select_sql(self, sql: str, auto_session=False) -> ResultStatus:
        """Run a SELECT SQL full text statement and returns the result.

        It is **assumed** a SELECT SQL statement, there is no check enforced.

        :param str sql: the full text SELECT SQL statement.

        :param bool auto_session: upon an operation on the underlying database, SQLAlchemy auto
            starts a transaction if there is not one in progress. If this method is in a 
            single call, the caller should set this param to True to get rid of the transaction 
            when finished: if the call was successful, the transaction is committed, otherwise 
            it rolls back. If it is called as a part of an ongoing transaction, in which case 
            SQLAlchemy does not start another transaction, then just ignore this param, the caller 
            is responsible for managing transaction atomicity.

        :return: `ResultStatus <https://bh-apistatus.readthedocs.io/en/latest/result-status.html>`_.

        Further illustrations of return value, as a dictionary.

        On successful::

            {
                "status": {
                    "code": 200,
                    "text": "Data has been retrieved successfully."                    
                },
                "data": [
                    {...},
                    ...,
                    {...}
                ]
            }

        where ``200`` is ``HTTPStatus.OK.value``. ``200`` does not mean the SELECT SQL 
        statement results in any data retrieved.

        On failure::

            {
                "status": {
                    "code": 500,
                    "text": "...error text..."
                }
            }

        where ``500`` is ``HTTPStatus.INTERNAL_SERVER_ERROR.value``.
        """

        logger.debug('Entered')
        try:
            status = {}

            # raise Exception('Test exception from db_funcs.run_select_sql(engine, sql) 1')

            result = self.session.execute(text(sql))

            # raise Exception('Test exception from db_funcs.run_select_sql(engine, sql) 2')

            data = json.loads(json.dumps([dict(row._mapping.items()) for row in result], \
                use_decimal=True, default=json_funcs.serialise, indent="  "))

            if (len(data) == 0):
                status = make_status(text=BH_SQL_NO_DATA_MSG)
            else:
                status = make_status(text=BH_RETRIEVED_SUCCESSFUL_MSG, data=data)

            if auto_session: self.commit_transaction()

        except Exception as e:
            logger.error(str(e))
            status = make_500_status(str(e))

            if auto_session: self.commit_transaction()

        finally:
            logger.debug('Exited.')

            if 'result' in locals():
                result.close()

            return status

class WriteCapableTable(ReadOnlyTable):
    """Implement an abstract base model (table) class which INSERT, UPDATE and DELETE
    functionalities.

    This table class should be the parent class for the majority of applications' tables, whom 
    the contents would change.

    In general, for this abstract class and its abstract descendant classes, do not 
    access :attr:`~bh_database.core.BaseSQLAlchemy.query` when not assigned. E.g.::

        assert WriteCapableTable.query == None

    It results in the following exception::

        ArgumentError("Column expression, FROM clause, or other columns clause element expected, <class 'bh_database.core.BaseSQLAlchemy'>.")
    """

    __abstract__ = True

    def run_execute_sql(self, sql: str, auto_session=False) -> ResultStatus:
        """Run an execute SQL full text statement and return a `ResultStatus 
        <https://bh-apistatus.readthedocs.io/en/latest/result-status.html>`_.

        An execute SQL is an UPDATE or a DELETE SQL statement. It is **assumed** an execute 
        SQL statement, there is no check enforced.

        :param str sql: the full text execute SQL statement.

        :param bool auto_session: upon an operation on the underlying database, SQLAlchemy auto
            starts a transaction if there is not one in progress. If this method is in a 
            single call, the caller should set this param to True to get rid of the transaction 
            when finished: if the call was successful, the transaction is committed, otherwise 
            it rolls back. If it is called as a part of an ongoing transaction, in which case 
            SQLAlchemy does not start another transaction, then just ignore this param, the caller 
            is responsible for managing transaction atomicity.

        :return: `ResultStatus <https://bh-apistatus.readthedocs.io/en/latest/result-status.html>`_.

        Further illustrations of return value, as a dictionary.

        On successful::

            {
                "status": {
                    "code": 200,
                    "text": ""
                }
            }        

        On failure::

            {
                "status": {
                    "code": 500,
                    "text": "...message text..."
                }
            }        
        """

        logger.debug('Entered')
        try:
            # raise Exception('Test exception from db_funcs.run_select_sql(engine, sql)')

            if auto_session: self.begin_transaction()

            result = self.session.execute(text(sql))

            # raise Exception('Test exception from db_funcs.run_select_sql(engine, sql)')

            status = make_status(text='')

            if auto_session: self.commit_transaction()

        except Exception as e:
            logger.error(str(e))

            status = make_500_status(str(e))

            if auto_session: self.rollback_transaction()

        finally:
            logger.debug('Exited.')

            if 'result' in locals():
                result.close()

            return status

    def __collate_data(self, result, dataset) -> list:
        columns = [column[0] for column in result.description]

        data = []
        for row in dataset:
            record = {}
            for idx, name in enumerate(columns):
                record[name] = row[idx]
            data.append(record)

        return data

    def run_stored_proc(self, stored_proc_name: str, params: list, auto_session=False) -> ResultStatus:
        """Execute a stored procedure which returns some data.

        It is **assumed** the stored procedure returns some data.

        :param stored_proc_name sql: the name of the stored procedure.

        :param list params: list of param values passed to the stored procedure.

        :param bool auto_session: upon an operation on the underlying database, SQLAlchemy auto
            starts a transaction if there is not one in progress. If this method is in a 
            single call, the caller should set this param to True to get rid of the transaction 
            when finished: if the call was successful, the transaction is committed, otherwise 
            it rolls back. If it is called as a part of an ongoing transaction, in which case 
            SQLAlchemy does not start another transaction, then just ignore this param, the caller 
            is responsible for managing transaction atomicity.

        :return: `ResultStatus <https://bh-apistatus.readthedocs.io/en/latest/result-status.html>`_.

        Further illustrations of return value, as a dictionary.

        On successful::

            {
                "status": {
                    "code": 200,
                    "text": "Data has been retrieved successfully."
                },
                "data": [
                    {...},
                    ...
                    {...}
                ]
            }        

        On failure::

            {
                "status": {
                    "code": 500,
                    "text": "...error text..."
                }
            }        
        """

        logger.debug('Entered')
        try:
            if auto_session: self.begin_transaction()
            
            with closing(self.session.connection().connection.cursor()) as cursor:
                cursor.callproc(stored_proc_name, params)

                # raise Exception('run_stored_proc_1() raises test exception...')

                match Database.database_type():
                    case DatabaseType.MySQL:
                        try:
                            result = next(cursor.stored_results())
                        except StopIteration:
                            msg = BH_STORED_PROC_NO_RESULT_SET_MSG.format(stored_proc_name)
                            status = make_status(text=msg)
                            
                            logger.error(msg)

                            return

                        dataset = result.fetchall()

                        if (len(dataset) == 0):
                            status = make_status(text=BH_SQL_NO_DATA_MSG)
                            return

                        data = self.__collate_data(result, dataset)

                    case DatabaseType.PostgreSQL:
                        dataset = cursor.fetchall()
                        data = self.__collate_data(cursor, dataset)

                    case DatabaseType.Unknown: 
                        raise Exception(BH_UNSUPPORTED_DATABASE_MSG.format(Database.driver_name()))

                status = make_status(text=BH_RETRIEVED_SUCCESSFUL_MSG)
                status.add_data(data=data)

                if auto_session: self.commit_transaction()

        except Exception as e:
            status = make_500_status(str(e))

            logger.error(str(e))

            if auto_session: self.rollback_transaction()

        finally:
            logger.debug('Exited.')

            if 'result' in locals():
                result.close()

            return status

    def __split_data(self, data: list, new_list: list, updated_list: list) -> None:
        for record in data:
            rec_status = record[BH_REC_STATUS_FIELDNAME]
            del record[BH_REC_STATUS_FIELDNAME]

            if rec_status == BH_RECORD_STATUS_NEW:
                new_list.append(record)

            elif rec_status == BH_RECORD_STATUS_MODIFIED:
                updated_list.append(record)

    def __get_next_id(self, tablename, columnname):
        sql = "select get_unique_id('{0}', '{1}') {1}".format(tablename, columnname)

        status = self.run_select_sql(sql)

        if (status.code == HTTPStatus.OK.value):
            if (not status.has_data) or (len(status.data) == 0): 
                status.text = BH_NEXT_ID_NO_RESULT_MSG.format(tablename, columnname)

        return status

    def __set_new_id(self, new_list: list) -> ResultStatus:
        """Getting new Ids for new records.

        If new records already have Ids set, then skip getting.
        """
        for record in new_list:
            """
            If primary key is in record, and its value is a valid integer, then don't get one.
            """
            if (self._primary_key in record) and (is_integer(record[self._primary_key])):
                continue

            id_status = self.__get_next_id(self.__tablename__, self._primary_key)
            if (id_status.code != HTTPStatus.OK.value):
                return make_500_status(id_status.text)

            record[self._primary_key] = id_status.data[0][self._primary_key]

        return make_status()

    def _insert(self, list):
        """Within a transaction, any database exception is not raised at this point,
        they will be raised when calling flush or commit the current transaction.
        Rollback the current transaction will not raise an exception, i.e. any database
        violations seem to be removed by the rollback.
        """
        for record in list:
            self.session.add(self._type(**record))

    def _update(self, list):
        """Within a transaction, any database exception is not raised at this point,
        they will be raised when calling flush or commit the current transaction.
        Rollback the current transaction will not raise an exception, i.e. any database
        violations seem to be removed by the rollback.
        """
        for entry in list:
            stmt = (
                update(self._type)
                .where(self._type.__table__.columns[self._primary_key] == entry[self._primary_key])
                .values(entry)
                .execution_options(synchronize_session="fetch")
          )
            self.session.execute(stmt)

    def write_to_database(self, data: list) -> ResultStatus:
        """Write new records and modified records to the underlying database table.

        When all data have been written, it will flush the transaction to cause any
        potential database violation to come out as an exception so that the result
        can be accurately determined, freeing the callers from having to handle any
        possible exception. Callers only have to check the returned result.

        Flushing the transaction also causes intermediate pending committed data be
        available, callers can access these without having to call flush_transcation().

        :Assumptions:

            1. The table has a single primary key of type integer.
            2. The database already has table ``unique_id`` and stored method ``get_unique_id`` \
                defined. Please see :ref:`getting-started-database-requirements` for more detail.

        :Transaction: callers must either call 
            :py:meth:`~bh_database.core.BaseSQLAlchemy.commit_transaction` 
            or :py:meth:`~bh_database.core.BaseSQLAlchemy.rollback_transaction` to 
            commit or rollback the write respectively. E.g.::

                Employees.begin_transaction(Employees)
                status = Employees().write_to_database([new_emp1, new_emp2])
                Employees.commit_transaction(Employees)

        :param list data: data contains both new records and updated records.

        An example of ``data``::

            [
            	{
                    "col_1": 999, ..., "col_n": "xxx",
                    "recStatus": "<new> | <modified>"
            	},
                ...,
            	{
                    "col_1": 999, ..., "col_n": "xxx",
                    "recStatus": "<new> | <modified>"
            	},
           ]           

        For each new record (row) in ``data``, if primary key is present, and has a valid 
        integer value, then a new unique integer Id is not requested. Otherwise, calls stored 
        method ``get_unique_id`` with the table name and primary key column name to get next 
        unique integer Id.
           
        :return: `ResultStatus <https://bh-apistatus.readthedocs.io/en/latest/result-status.html>`_.

        Further illustrations of return value, as a dictionary.

        On successful::

            {
                "status": {
                    "code": 200,
                    "text": "Data has been saved successfully."
                },
                "{__tablename__}_new_list": [
                    {...}, ... ,{}
                ],
                "{__tablename__}_updated_list": [
                    {...}, ... ,{}
                ]
            }

        ``__tablename__``: i.e. ``invoice``, ``service``, etc. E.g.:

            | ``service_new_list``
            | ``service_updated_list``

        Either ``{__tablename__}_new_list`` or ``{__tablename__}_updated_list`` can be empty, 
        but not both. At least one list must have a single object in it.

        Record/row objects in these lists have ``recStatus`` removed.

        On failure::

            {
                "status": {
                    "code": 500,
                    "text": "...error text..."
                }
            }

        See the following test modules for more info:

            * ./tests/test_25_base_table_crud_methods_postgresql.py
            * ./tests/test_26_base_table_crud_methods_mysql.py
        """

        logger.debug('Entered')
        try:            
            # Prepares list of new records and updated records.
            new_list = []
            updated_list = []

            self.__split_data(data, new_list, updated_list)

            # raise Exception('WriteCapableTable::write_to_database(...) test exception...')

            # Getting new Ids for new records.
            status = self.__set_new_id(new_list)

            if (status.code != HTTPStatus.OK.value): return

            if len(new_list) > 0:
                self._insert(new_list)

            if len(updated_list) > 0:
                self._update(updated_list)

            # 
            # This is to cause any potential database violation to raise exception, so
            # that it will be handled by the exception block below: callers just have
            # to work with the returned result.
            #
            self.session.flush()

            status = make_status(text=BH_SAVED_SUCCESSFUL_MSG)
            status.add_data(new_list, '{}_new_list'.format(self.__tablename__.lower()))
            status.add_data(updated_list, '{}_updated_list'.format(self.__tablename__.lower()))

        except Exception as e:
            logger.error(str(e))
            
            status = make_500_status(str(e))

        finally:
            logger.debug('Exited.')
            return status
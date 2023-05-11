"""Core database wrapper classes for SQLAlchemy.

These classes currently support only two database types: MySQL and PostgreSQL. Drivers 
required, respectively:

    * `https://pypi.org/project/mysql-connector-python/ <https://pypi.org/project/mysql-connector-python/>`_.
    * `https://pypi.org/project/psycopg2/ <https://pypi.org/project/psycopg2/>`_.

Later classes, see module :py:doc:`base_table`, which implement base models (tables) that 
provide wrapper methods to run full SQL statements, and stored methods. There are some 
differences between drivers on stored methods execution, that is why only MySQL and PostgreSQL 
are supported presently. Internally, when executing stored methods, the codes use the connection
URL to determine which database it is to extract result set.

Classes in this module provide the following functionalities:

    * Database connection management. See :py:class:`Database`.

    * A custom SQLAlchemy query class which implements paginating. See :py:class:`BaseQuery` \
        and :py:class:`~bh_database.paginator.Paginator`.

    * A generic :py:class:`BaseSQLAlchemy` base model (table), which should be the **indirect** \
        base model for applications' models. This class encapsulates:
        
        * SQLAlchemy scoped session, thereby providing methods to implement transaction atomicity.
        * A custom base query with paginating ability mentioned above.
        * Fully implemented dunder methods str() and repr(), which are implemented by class \
            :py:class:`BaseModel`: one of the base classes of :py:class:`BaseSQLAlchemy`.

    * A generic SQLAlchemy declarative base class :py:class:`Base` which should include \
        all required metaclasses.

Applications should not be **directly** interested in the :py:class:`BaseSQLAlchemy` base model 
(table). Module :py:doc:`base_table` defines two application-ready base model classes 
:py:class:`.base_table.ReadOnlyTable` and :py:class:`.base_table.WriteCapableTable`. Applications'
models should descend from either one of these as appropriate.

From this module, the only class which applications should call directly is :py:class:`Database`.
To connect to a database server, applications should not have do not more than::

    # Getting rid of any residual connection. If we are absolutely sure there is none, 
    # then there is no need for this call.
    Database.disconnect()
    Database.connect(db_url, [schema | None])
"""

import logging
# from threading import get_ident
from enum import Enum

from http import HTTPStatus

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker, 
    scoped_session,
    declarative_base,
    close_all_sessions,
    Query,
)
from sqlalchemy.orm.decl_api import DeclarativeMeta

from bh_apistatus.result_status import ResultStatus

from bh_database.paginator import Paginator

#: 
Base = declarative_base(metaclass=DeclarativeMeta)

class BaseQuery(Query):
    """Custom base query class.

    Provide pagination capability for `SQLAlchemy Query Object <https://docs.sqlalchemy.org/en/14/orm/query.html>`_.

    All models (tables) descend from :py:class:`BaseSQLAlchemy` will have their class attribute
    :attr:`~.BaseSQLAlchemy.query` set to this custom query class, therefore, automatically has 
    pagination capability.
    """
    def paginate(self, page: int, per_page: int) -> Paginator:
        """Pagination method.

        :param int page: the page number to retrieve data for.

        :param int per_page: how many records to retrieve for each page.

        :return: a :py:class:`.paginator.Paginator` instance.
        """
        return Paginator(self, page, per_page).execute()
    
class BaseModel(object):
    """A custom base model / table class for `SQLAlchemy declarative base model 
    <https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html>`_.

    All models (tables) descend from :py:class:`BaseSQLAlchemy` will have this custom base
    model as one of the base classes.

    This class basically implements two (2) magic methods:
    `object.__str__(self) <https://docs.python.org/3/reference/datamodel.html#object.__str__>`_;
    and 
    `object.__repr__(self) <https://docs.python.org/3/reference/datamodel.html#object.__repr__>`_.

    For an usage example, see ``./tests/test_20_base_table_dunder.py``.
    """

    def __str__(self):
        fmt = u'{}: {}'
        class_ = self.__class__.__name__
        attrs = [(k, getattr(self, k)) for k in self.__mapper__.columns.keys()]

        sattrs = u', '.join('{}: {!r}'.format(*x) for x in attrs)
        return fmt.format(class_, sattrs)

    def __repr__(self):
        fmt = u'{}({})'
        class_ = self.__class__.__name__

        attrs = [(k, getattr(self, k)) for k in self.__mapper__.columns.keys()]

        sattrs = u', '.join('{}={!r}'.format(*x) for x in attrs)

        return fmt.format(class_, sattrs)
    
class BaseSQLAlchemy(Base, BaseModel):
    """The parent most class for all models / tables.

    Provide methods to implement transaction atomicity.

    Class attributes:
        | session = None. When set, is of type `sqlalchemy.orm.session.Session <https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session>`_.
        | query = None. When set, is of type :py:class:`BaseQuery`.

    In general, for this abstract class and its abstract descendant classes, do not 
    access :attr:`query` when not assigned. E.g.::

        assert core.BaseSQLAlchemy.query == None

    It results in the following exception::

        ArgumentError("Column expression, FROM clause, or other columns clause element expected, <class 'bh_database.core.BaseSQLAlchemy'>.")
    """

    __abstract__ = True

    #: Class attribute. When set, is of type `sqlalchemy.orm.session.Session <https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session>`_.
    session = None
    #: Class attribute. When set, is of type :py:class:`BaseQuery`.    
    query = None

    def begin_transaction(self):
        """Start a new transaction.
        """
        if not self.session.in_transaction(): self.session.begin()

    def flush_transaction(self):
        """Flush an ongoing transaction.

        Make intermediate results available so that they can be accessed while the transaction 
        is still on going. An example of intermediate result is a new unique key value, this 
        value might be needed as a foreign key for detail records awaiting written.

        :Note on Exception: 

        Potential unhandled exception: caller must handle the exception.

        Within an ongoing transaction, if there is any potential database violation, calling 
        this method will cause the driver to raise exception on the violation.
        """
        self.session.flush()

    def commit_transaction(self):
        """Commit a current transaction.

        :Note on Exception: 

        Potential unhandled exception: caller must handle the exception.

        Within an ongoing transaction, if there is any potential database violation, calling 
        this method will cause the driver to raise exception on the violation.

        It is recommended to call :py:meth:`~finalise_transaction` instead.
        """
        self.session.commit()
        self.session.close()

    def rollback_transaction(self):
        """Rollback a current transaction.

        When absolutely certain that the ongoing transaction must be rolled back, then call
        this method. Otherwise it is recommended to call :py:meth:`~finalise_transaction` 
        instead.
        """
        self.session.rollback()
        self.session.close()

    def finalise_transaction(self, status: ResultStatus):
        """Commit or rollback a transaction based on ``status.code``.

        :param ResultStatus status: result of the last CRUD call. \
            `ResultStatus <https://bh-apistatus.readthedocs.io/en/latest/result-status.html>`_.
        """
        self.commit_transaction() \
            if (status.code == HTTPStatus.OK.value ) else self.rollback_transaction()

class DatabaseType(Enum):
    """Enumerated constants identifying supported databases.

    Define some enumerations for the supported database servers.
    """    
    Unknown = -1
    MySQL = 1
    PostgreSQL = 2

class Database:
    """Provide database connection management.

    Applications should not instantiate this class. It is semantically a *static* class.
    
    All applications proper models (tables) should descend from :py:class:`BaseSQLAlchemy`.
    The :py:meth:`~connect` method sets both :py:class:`BaseSQLAlchemy` class attributes 
    :attr:`~.BaseSQLAlchemy.session` and :attr:`~.BaseSQLAlchemy.query`, armed with these
    attributes, application models have sufficient means to carry out CRUD operations. 

    Thus, to connect to a database server, applications should not have do not more than::

        # Getting rid of any residual connection. If we are absolutely sure there is none, 
        # then there is no need for this call.
        Database.disconnect()
        Database.connect(db_url, [schema | None])

    See the following tests for more info:

            * ``./tests/test_05_core_basesqlalchemy_postgresql.py``
            * ``./tests/test_06_core_basesqlalchemy_mysql.py``

    Class attributes:
        | engine = None. When set, is of type `sqlalchemy.future.engine.Engine <https://docs.sqlalchemy.org/en/14/core/future.html>`_.
        | session_factory = None. When set, is of type `sqlalchemy.orm.sessionmaker <https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker>`_.
        | database_session = None. When set, is of type `sqlalchemy.orm.scoping.scoped_session <https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session>`_.

    For a usage example, see ``./tests/test_01_core_database_postgresql.py`` and 
    ``./tests/test_02_core_database_mysql.py``.
    """

    #: Class attribute. When set, is of type `sqlalchemy.future.engine.Engine <https://docs.sqlalchemy.org/en/14/core/future.html>`_.
    engine = None
    #: Class attribute. When set, is of type `sqlalchemy.orm.sessionmaker <https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker>`_.
    session_factory = None
    #: Class attribute. When set, is of type `sqlalchemy.orm.scoping.scoped_session <https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session>`_.
    database_session = None

    @staticmethod
    def database_type(db_url=None) -> DatabaseType:
        """Return an enum which represents a supported database server type.

        :param str db_url: optional. A valid database connection string. If not specified, then the 
            current database connection string is used. That means, if this param is specified, then 
            a valid database connection is not required.

        :return: a :py:class:`DatabaseType`'s enum.

        :raises AttributeError: if not connected to a database, i.e. invalid database connection, and
            param ``db_url`` is not specified.
        """
        url_str = db_url if (db_url != None) else Database.engine.url.drivername

        if 'mysql' in url_str: return DatabaseType.MySQL
        elif 'postgresql' in url_str: return DatabaseType.PostgreSQL
        else: return DatabaseType.Unknown

    @staticmethod
    def driver_name() -> str: 
        """Return the driver name of the current database connection.

        :return: The driver name of the current database connection. E.g. \
            if the connection string is ``"postgresql+psycopg2://postgres:<password>@localhost/employees"``,
            then the returned value is ``postgresql+psycopg2``.
        :rtype: str.

        :raises AttributeError: if not connected to a database, i.e. invalid database connection.
        """
        return Database.engine.url.drivername

    @staticmethod
    def connect(db_url: str, schema: str) -> None:
        """Establish a connection to a database server.

        :param str db_url: a valid database connection string.
        :param str schema: the database schema in the database to connect to. Presently only 
            required if connecting to a PostgreSQL database.

        Create the following class attributes :attr:`~.engine`, :attr:`~.session_factory` 
        and scoped session :attr:`~.database_session`.

        Also, set both ``BaseSQLAlchemy``'s :attr:`~.BaseSQLAlchemy.session` and
        :attr:`~.BaseSQLAlchemy.query` as::

            BaseSQLAlchemy.session = Database.database_session(future=True)
            BaseSQLAlchemy.query = Database.database_session.query_property(BaseQuery)

        ``BaseSQLAlchemy``'s :attr:`~.BaseSQLAlchemy.query` is still ``None`` after this assignment. 
        IT IS POSTULATING THAT, this is because :py:class:`BaseSQLAlchemy` is abstract, which means 
        it does not have an associated database table declared. *Postulating* because there is not an
        official document confirms that this is the case. See the following test modules for more info:

            * ``./tests/test_15_base_table_postgresql.py``
            * ``./tests/test_16_base_table_mysql.py``

        Application models, i.e. tables, descend indirectly from :py:class:`BaseSQLAlchemy`, and hence
        inherits class attributes :attr:`~.BaseSQLAlchemy.session` and :attr:`~.BaseSQLAlchemy.query`.
        Table classes use these two class attributes to talk to the connected database: **they should 
        not need the** :py:class:`Database` **class for anything else**.
        """
        logger = logging.getLogger('trx')

        info_str_fmt = "{}: \n{:16}: {!r}\n{:16}: {!r}\n{:16}"

        logger.debug(info_str_fmt.format("Before", "engine", id(Database.engine), "session_factory", 
            id(Database.session_factory), "database_session", id(Database.database_session)))

        if (Database.engine == None):
            args = {}
            if (Database.database_type(db_url) == DatabaseType.PostgreSQL):
                args={"options": f"-csearch_path={schema}"}
            Database.engine = create_engine(db_url, echo=False, echo_pool=False, future=True, connect_args=args)
            #
            # <class 'sqlalchemy.future.engine.Engine'>
            #

            """
            Assert database connection is valid: caller needs to handle exception.
            """
            Database.engine.connect()

        if (Database.session_factory == None): 
            Database.session_factory = sessionmaker(autocommit=False, autoflush=False, \
                    bind=Database.engine, future=True)

        if (Database.database_session == None):
            # Database.database_session = scoped_session(Database.session_factory, scopefunc=get_ident)
            Database.database_session = scoped_session(Database.session_factory)

        BaseSQLAlchemy.session = Database.database_session(future=True)
        """
        BaseSQLAlchemy.query is still None after the assignment. I AM POSTULATING THAT
        it is because BaseSQLAlchemy is abstract, which means it does not have an 
        associated database table declared.
        """
        BaseSQLAlchemy.query = Database.database_session.query_property(BaseQuery)

        logger.debug(info_str_fmt.format("After", "engine", id(Database.engine), "session_factory", 
            id(Database.session_factory), "database_session", id(Database.database_session)) )

    @staticmethod
    def disconnect() -> None:
        """Disconnect from database.

        Remove the scoped session, close all connections, dispose the connection pool used by the engine
        (i.e. calling `sqlalchemy.engine.Engine.dispose(close: bool = True) -> None
        <https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.dispose>`_).

        Then set class attributes :attr:`~.database_session`, :attr:`~.session_factory` and
        :attr:`~.engine` to ``None``.

        Finally, set both ``BaseSQLAlchemy``'s :attr:`~.BaseSQLAlchemy.session` and 
        :attr:`~.BaseSQLAlchemy.query` class attributes to ``None`` also.

        Note, any scoped sessions, queries, etc. created locally via 
        :attr:`~.database_session` are *still* valid after calling this method.
        That is::

            POSTGRESQL_DB_URL = "postgresql+psycopg2://postgres:<password>@localhost/employees"
            POSTGRESQL_DB_SCHEMA = "employees"

            SELECT_EMPLOYEES = ("select * from employees where (upper(last_name) like '%NAS%')" 
                " and (upper(first_name) like '%AN') order by emp_no;")

            Database.connect(POSTGRESQL_DB_URL, POSTGRESQL_DB_SCHEMA)

            session = Database.database_session()
            query = Database.database_session.query_property(BaseQuery)
            other_session = Database.database_session()

            Database.disconnect()

            assert session != None
            assert query != None
            assert other_session != None

            result = session.execute(text(SELECT_EMPLOYEES))
            # result is CursorResult.
            assert result.rowcount == 38

            result = other_session.execute(text(SELECT_EMPLOYEES))
            # result is CursorResult.
            assert result.rowcount == 38
        """
        if (Database.database_session != None): Database.database_session.remove()

        close_all_sessions()
        
        if (Database.engine != None): Database.engine.dispose()

        Database.database_session = None
        Database.session_factory = None
        Database.engine = None

        BaseSQLAlchemy.session = None
        BaseSQLAlchemy.query = None

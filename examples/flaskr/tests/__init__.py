"""
Tests helper functions.
"""

"""    
Creates SQLAlchemy engine, session factory, scoped session, declarative 
base. Database entities are independent of the application instance. For
the application, see F:\bh_database\examples\flask\src\flaskr\__init__.py.
"""

from flaskr.config import get_config
from bh_database.core import Database

"""
This initial block will run once for tests:

    venv\Scripts\pytest.exe -k _unit_ -v
    venv\Scripts\pytest.exe -k _bro_ -v
    venv\Scripts\pytest.exe -k _integration_ -v
    venv\Scripts\pytest.exe
    venv\Scripts\pytest.exe -m <valid mark>

But the test app() fixture also creates an application instance, and so
create_database_entities(...) is called for each fixture call. But once entities have
been created, they will not be recreated upon subsequent calls during the same test
run.
"""

config = get_config()

Database.disconnect()
Database.connect(config.SQLALCHEMY_DATABASE_URI, config.SQLALCHEMY_DATABASE_SCHEMA)

from flaskr.models.employees import Employees

def delete_employee(partial_last_name: str, partial_first_name: str):
    Employees.begin_transaction(Employees)

    employees = Employees.session.query( Employees ).filter( 
        Employees.last_name.ilike(partial_last_name),
        Employees.first_name.ilike(partial_first_name)
    ).all()

    if ( employees != None ):
        for emp in employees:
            Employees.session.delete( emp )

    Employees.commit_transaction(Employees)
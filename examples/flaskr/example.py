# 01/05/2024.
#
# (venv) F:\bh_database\examples\flaskr>venv\Scripts\flask.exe --app example run --host 0.0.0.0 --port 5000
#
# http://localhost:5000/employees/search/%nas%/%An
#

from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
)

import flask

from bh_database.core import Database
from bh_database.base_table import WriteCapableTable

from bh_apistatus.result_status import ResultStatus

SQLALCHEMY_DATABASE_SCHEMA = 'employees'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:pcb.2176310315865259@localhost:3306/employees'
# Enable this for PostgreSQL.
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:pcb.2176310315865259@localhost/employees'

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

def create_app(config=None):
    """Construct the core application."""

    app = flask.Flask(__name__, instance_relative_config=False)

    init_extensions(app)
    
    init_app_database(app)

    return app
    
def init_extensions(app):
    app.url_map.strict_slashes = False

def init_app_database(app):    
    Database.disconnect()
    Database.connect(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_DATABASE_SCHEMA)

app = create_app()

@app.get('/employees/search/<last_name>/<first_name>')
def search_employees(last_name: str, first_name: str) -> dict:
    """ last_name and first_name are partial using %.

    An example of a valid route: http://localhost:5000/employees/search/%nas%/%An
    """

    return Employees() \
        .select_by_partial_last_name_and_first_name(last_name, first_name) \
        .as_dict()

if __name__ == '__main__':  
   app.run()
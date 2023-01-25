"""
Tests helper functions.
"""

from bh_database.core import Database

POSTGRESQL_DB_URL = "postgresql+psycopg2://postgres:pcb.2176310315865259@localhost/employees"
POSTGRESQL_DB_SCHEMA = "employees"
MYSQL_DB_URL = "mysql+mysqlconnector://root:pcb.2176310315865259@localhost/employees"

def create_postgresql_database_entities():
    Database.connect(POSTGRESQL_DB_URL, POSTGRESQL_DB_SCHEMA)

def create_mysql_database_entities():
    Database.connect(MYSQL_DB_URL, None)

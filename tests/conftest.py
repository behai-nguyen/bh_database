"""
pytest entry.

To run all tests:

1. venv\Scripts\python.exe -m pytest
2. venv\Scripts\pytest.exe

To run individual tests:

venv\Scripts\pytest.exe -m <@pytest.mark>

Valid @pytest.marks are defined in pytest.ini.
"""

import pytest

from bh_database.core import Database

from tests import (
    create_mysql_database_entities,
    create_postgresql_database_entities,
)

@pytest.fixture(scope='module')
def mysql():
    Database.disconnect()
    create_mysql_database_entities()

@pytest.fixture(scope='module')
def postgresql():
    Database.disconnect()
    create_postgresql_database_entities()

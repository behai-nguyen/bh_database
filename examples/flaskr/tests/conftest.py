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

from flaskr.config import get_config
from flaskr import create_app

@pytest.fixture(scope='module')
def app():
    app = create_app(get_config())

    app.app_context().push()

    return app

@pytest.fixture(scope='module')
def test_client(app):
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        """
        See: https://github.com/pytest-dev/pytest-flask/issues/69 
		Sessions are empty when testing #69 
        """
        with testing_client.session_transaction() as session:
            session['Authorization'] = 'redacted'

        yield testing_client  # this is where the testing happens!

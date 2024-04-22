"""
Application package.
"""
import flask

"""
from flask_session import Session

from flask_bcrypt import Bcrypt

from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager
"""

import logging
import logging.config

from flaskr.config import get_config

from bh_database.core import Database

"""
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auths.login'
login_manager.login_message_category = 'info'

bcrypt = Bcrypt()
"""

# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()

def create_app(config=None):
    """Construct the core application."""

    app = flask.Flask(__name__, instance_relative_config=False)

    app.config.from_object(get_config())

    init_extensions(app)
    # register_loggers()
    
    init_app_database(app)

    """
    init_csrf(app)
    register_blueprints(app)
    """

    from .controllers import employees_admin
    app.register_blueprint(employees_admin.bp)

    return app
    
def init_extensions(app):
    app.url_map.strict_slashes = False

    """
    login_manager.init_app(app)
    bcrypt.init_app(app)
    """

"""
def register_loggers():
    with open('omphalos-logging.yml', 'rt') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
"""

def init_app_database(app):
    """    
    Creates SQLAlchemy engine, session factory, scoped session, declarative base.
    Database entities are independent of the application instance.
    """
    
    Database.disconnect()
    Database.connect(app.config["SQLALCHEMY_DATABASE_URI"], \
            app.config["SQLALCHEMY_DATABASE_SCHEMA"])

"""
def init_csrf(app):
    csrf.init_app(app)

def register_blueprints(app):
    from book_keeping import urls

    for blueprint in urls.blueprints:
        app.register_blueprint(blueprint)
"""
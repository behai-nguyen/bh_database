"""
Application package.
"""

import os

import logging
import logging.config
import yaml

import flask

from flaskr.config import get_config

from bh_database.core import Database

def create_app(config=None):
    """Construct the core application."""

    app = flask.Flask(__name__, instance_relative_config=False)

    app.config.from_object(get_config())

    init_extensions(app)

    prepare_logging_and_start_listener()

    init_app_database(app)
    
    from .controllers import employees_admin
    app.register_blueprint(employees_admin.bp)

    logging.getLogger('flaskr.example').info("FlaskR example startup complete.")

    return app
    
def init_extensions(app):
    app.url_map.strict_slashes = False

def retrieve_queue_listener():
    """
    Retrieves and returns the QueueListener instance associated with 
    the 'queue_rotating_file' handler.
    """
    return logging.getHandlerByName('queue_rotating_file').listener

def prepare_logging_and_start_listener():
    """
    1. Ensures ./logs sub-directory exists under script root directory.
    2. Loads the logger config YAML file and prepares the logging config.
    3. Retrieves and returns the QueueListener instance associated with 
       the 'queue_rotating_file' handler.
    """

    # Ensure ./logs sub-directory exists under script root directory.
    os.makedirs(f".{os.sep}logs", exist_ok=True)

    # Now that ./logs sub-directory exists under script root directory,
    # loads the logger config YAML file and prepares the logging dictionary
    # config.
    with open('logger_config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

    listener = retrieve_queue_listener()
    listener.start()        

def init_app_database(app):
    """    
    Creates SQLAlchemy engine, session factory, scoped session, declarative base.
    Database entities are independent of the application instance.
    """

    Database.disconnect()

    # It is the responsibility of the caller to handle this exception.
    logger = logging.getLogger('flaskr.example')
    try:
        Database.connect(app.config["SQLALCHEMY_DATABASE_URI"], \
            app.config["SQLALCHEMY_DATABASE_SCHEMA"])
    except Exception as e:
        logger.exception(str(e))
        logger.error('Attempt to terminate the application now.')
        # os.kill(...) would not flush the above two loggings.
        # os.kill(os.getpid(), signal.SIGINT)
        
        # raise RuntimeError(...) flushes any pending loggings and 
        # also terminates the application.
        raise RuntimeError('Failed to connect to the target database.')

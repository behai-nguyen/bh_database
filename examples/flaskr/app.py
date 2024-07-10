"""
App entry point.
"""

import logging

import atexit

from bh_database.core import Database

from flaskr import create_app

from flaskr.controllers.employees_admin import search_form

app = create_app()

@app.route("/")
def index():
    return search_form()

@atexit.register
def app_shutdown():
    from flaskr import retrieve_queue_listener

    Database.disconnect()

    logger = logging.getLogger('flaskr.example')

    logger.info("FlaskR example is shutting down...")
    logger.info("Logging queue listener will stop listening...")

    listener = retrieve_queue_listener()
    listener.stop()
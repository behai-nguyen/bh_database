# 28/04/2024
#
# (venv) F:\fastapi\emp>..\venv\Scripts\uvicorn.exe main:app --reload
# 
#

import os
from contextlib import asynccontextmanager

import logging
import logging.config
import yaml

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from bh_database.core import Database
from fastapir.config import get_config

from fastapir.controllers import employees_admin

def __retrieve_queue_listener():
    """
    Retrieves and returns the QueueListener instance associated with 
    the 'queue_rotating_file' handler.
    """
    return logging.getHandlerByName('queue_rotating_file').listener

def prepare_logging_and_start_listener(default_path='logger_config.yaml'):
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
    with open(default_path, 'r') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

    listener = __retrieve_queue_listener()
    listener.start()

prepare_logging_and_start_listener()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger('fastapir.example')

    Database.disconnect()

    # It is the responsibility of the caller to handle this exception.
    try:
        Database.connect(cfg.SQLALCHEMY_DATABASE_URI, cfg.SQLALCHEMY_DATABASE_SCHEMA)
    except Exception as e:
        logger.exception(str(e))
        logger.error('Attempt to terminate the application now.')
        # raise RuntimeError(...) flushes any pending loggings and 
        # also terminates the application.        
        raise RuntimeError('Failed to connect to the target database.')        

    logger.info("FastAPI example startup complete.")

    yield

    Database.disconnect()

    logger.info("FastAPI example is shutting down...")
    logger.info("Logging queue listener will stop listening...")

    listener = __retrieve_queue_listener()
    listener.stop()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/fastapir/static"), name="static")

app.include_router(employees_admin.router)

cfg = get_config()

@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def search_form(request: Request):
    return await employees_admin.search_form(request)

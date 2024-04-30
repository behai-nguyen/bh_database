"""
Flask configuration variables.
"""
from os import (
    getcwd, 
    environ, 
    path,
)
	
from dotenv import load_dotenv

basedir = getcwd()
load_dotenv( path.join(basedir, '.env') )

class Config:
    """Set configuration from .env file."""

    # General Config: not used in FastAPI.
    SECRET_KEY = environ.get( 'SECRET_KEY' )

    # Database.
    SQLALCHEMY_DATABASE_URI = environ.get( 'SQLALCHEMY_DATABASE_URI' )
    SQLALCHEMY_DATABASE_SCHEMA = environ.get( 'SQLALCHEMY_DATABASE_SCHEMA' )

def get_config():
    return Config()
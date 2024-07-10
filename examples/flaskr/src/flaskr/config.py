"""
Flask configuration variables.
"""
from os import (
    getcwd, 
    environ, 
    path,
)
	
from dotenv import load_dotenv

from bh_utils.conversions import str_to_bool

basedir = getcwd()
load_dotenv( path.join(basedir, '.env') )

class Config:
    """Set Flask configuration from .env file."""

    # General Config.
    SECRET_KEY = environ.get( 'SECRET_KEY' )
    FLASK_APP = environ.get( 'FLASK_APP' )
    FLASK_DEBUG = str_to_bool( environ.get('FLASK_DEBUG') )

    # Database.
    SQLALCHEMY_DATABASE_URI = environ.get( 'SQLALCHEMY_DATABASE_URI' )
    SQLALCHEMY_DATABASE_SCHEMA = environ.get( 'SQLALCHEMY_DATABASE_SCHEMA' )

def get_config():
    return Config()
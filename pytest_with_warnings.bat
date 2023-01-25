@echo off

REM
REM 17/01/2022.
REM 
REM Migrating to SQLAlchemy 2.0. Flush out warnings MovedIn20Warning.
REM https://stackoverflow.com/questions/68078937/sqlalchemy-2-0-migration-how-to-turn-on-warn-20
REM SQLAlchemy 2.0 migration: how to turn on warn_20
REM 

set SQLALCHEMY_WARN_20=1
venv\Scripts\python.exe -W always::DeprecationWarning -m pytest
# 28/04/2024
#
# (venv) F:\fastapi\emp>..\venv\Scripts\uvicorn.exe main:app --reload
# 
#

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from bh_database.core import Database
from fastapir.config import get_config

from fastapir.controllers import employees_admin

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/fastapir/static"), name="static")

app.include_router(employees_admin.router)

cfg = get_config()

Database.disconnect()
Database.connect(cfg.SQLALCHEMY_DATABASE_URI, cfg.SQLALCHEMY_DATABASE_SCHEMA)

@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def search_form(request: Request):
    return await employees_admin.search_form(request)

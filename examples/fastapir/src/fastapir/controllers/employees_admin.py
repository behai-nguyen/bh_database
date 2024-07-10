"""
Application employees administration functionalities controller.
"""
from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
)

from fastapir import logger

from fastapir.business.employees_mgr import EmployeesManager

from fastapir.controllers import templates

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)

@router.get("/search/{last_name}/{first_name}", response_class=HTMLResponse)
@router.post("/search/{last_name}/{first_name}", response_class=HTMLResponse)
async def search(request: Request, last_name: str, first_name: str):
    """ Production implementation would have authentication mechanism 
    in place to check for authenticated requests.

    Actual valid route:

    http://localhost:5000/employees/search/%nas%/%An    
    """

    logger.debug(f"Path: {request.url}")

    status = EmployeesManager() \
        .select_by_partial_last_name_and_first_name(last_name, first_name)
    
    return templates.TemplateResponse(request=request, 
                                      name="admin/emp_search_result.html",
                                      context={"status": status.as_dict()})

@router.get("/edit/{emp_no}", response_class=HTMLResponse)
async def edit(request: Request, emp_no: str):
    """ Production implementation would have authentication mechanism 
    in place to check for authenticated requests.

    Actual valid route:

    http://localhost:5000/employees/edit/10399
    """

    logger.debug(f"Path: {request.url}")

    status = EmployeesManager().select_by_employee_number(int(emp_no))
    
    return templates.TemplateResponse(request=request, 
                                      name="admin/emp_edit.html",
                                      context={"employee": status.serialise_data()})

@router.get("/search-by-emp-no/{emp_no}", response_class=JSONResponse)
async def search_by_emp_no(request: Request, emp_no: str):
    """ Production implementation would have authentication mechanism 
    in place to check for authenticated requests.

    Actual valid route:

    http://localhost:5000/employees/search-by-emp-no/10399
    """

    logger.debug(f"Path: {request.url}")

    return EmployeesManager().select_by_employee_number(int(emp_no)).as_dict()

@router.post("/save", response_class=JSONResponse)
async def save(request: Request):
    """ empNo can be blank, None or completely absent. 

    Actual valid route:

    http://localhost:5000/employees/save
    """

    logger.debug(f"Path: {request.url}")

    form = await request.form()

    return EmployeesManager().write_to_database(form._dict).as_dict()
 
@router.get("/new", response_class=HTMLResponse)
async def new(request: Request):
    """ Production implementation would have authentication mechanism 
    in place to check for authenticated requests.

    Actual valid route:

    http://localhost:5000/employees/new
    """

    logger.debug(f"Path: {request.url}")

    return templates.TemplateResponse(request=request, name="admin/emp_edit.html")

@router.get("/", response_class=HTMLResponse)
@router.post("/", response_class=HTMLResponse)
async def search_form(request: Request):
    """ Production implementation would have authentication mechanism 
    in place to check for authenticated requests.

    Actual valid route:

    http://localhost:5000/employees
    """

    logger.debug(f"Path: {request.url}")

    return templates.TemplateResponse(request=request, name="admin/emp_search.html")

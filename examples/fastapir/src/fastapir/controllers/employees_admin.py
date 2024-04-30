"""
Application employees administration functionalities controller.
"""
from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
)

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

    return EmployeesManager().select_by_employee_number(int(emp_no)).as_dict()

@router.post("/save", response_class=JSONResponse)
async def save(empNo: Annotated[int | None, Form()] = None,
    birthDate: Annotated[str, Form()] = ...,
    firstName: Annotated[str, Form()] = ...,
    lastName: Annotated[str, Form()] = ...,
    gender: Annotated[str, Form()] = ...,
    hireDate: Annotated[str, Form()] = ...):
    """ empNo can be blank, None or completely absent. Not setting it
    to optional will cause the server to return 500. It is the first
    in the form, endpoint's params must match form fields order, 
    therefore every other fields are set to required with ``...``, 
    this causes the fields not marked as required in the Swagger UI 
    doc [http://localhost:5000/docs](http://localhost:5000/docs)!

    This is contradictory to:

    > If you hadn't seen that ``...`` [part of Python and is called "Ellipsis"](https://docs.python.org/3/library/constants.html#Ellipsis).
    >
    > It is used by Pydantic and FastAPI to explicitly declare that a value is required.

    See [https://fastapi.tiangolo.com/tutorial/query-params-str-validations/](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/).
    
    Production implementation would have authentication mechanism 
    in place to check for authenticated requests.

    Actual valid route:

    http://localhost:5000/employees/save
    """

    params = {"empNo": empNo,
        "birthDate": birthDate,
        "firstName": firstName,
        "lastName": lastName,
        "gender": gender,
        "hireDate": hireDate
    }

    return EmployeesManager().write_to_database(params).as_dict()
 
@router.get("/new", response_class=HTMLResponse)
async def new(request: Request):
    """ Production implementation would have authentication mechanism 
    in place to check for authenticated requests.

    Actual valid route:

    http://localhost:5000/employees/new
    """

    return templates.TemplateResponse(request=request, name="admin/emp_edit.html")

@router.get("/", response_class=HTMLResponse)
@router.post("/", response_class=HTMLResponse)
async def search_form(request: Request):
    """ Production implementation would have authentication mechanism 
    in place to check for authenticated requests.

    Actual valid route:

    http://localhost:5000/employees
    """

    return templates.TemplateResponse(request=request, name="admin/emp_search.html")

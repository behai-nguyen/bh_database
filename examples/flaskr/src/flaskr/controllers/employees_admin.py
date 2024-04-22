"""
Application employees administration functionalities controller.
"""

from flask import (
    Blueprint,
    request,
    render_template,
    make_response,
)

from flaskr.business.employees_mgr import EmployeesManager

bp = Blueprint('employees', __name__, url_prefix='/employees', template_folder='templates')

@bp.route('/search/<last_name>/<first_name>', methods=['GET', 'POST'])
def search(last_name: str, first_name: str):
    """ Production implementation would have decorators, at the very least:

    @login_required

    Actual valid routes:

    http://localhost:5000/employees/search/%nas%/%An    
    """
    status = EmployeesManager() \
        .select_by_partial_last_name_and_first_name(last_name, first_name)
    
    html = render_template('admin/emp_search_result.html', status=status.as_dict())

    return make_response(html)

@bp.route('/edit/<emp_no>', methods=['GET'])
def edit(emp_no: str):
    """ Production implementation would have decorators, at the very least:

    @login_required

    Actual valid routes:

    http://localhost:5000/employees/edit/10399
    """

    status = EmployeesManager().select_by_employee_number(int(emp_no))
    
    html = render_template('admin/emp_edit.html', employee=status.serialise_data())
    return make_response(html)

@bp.route('/search-by-emp-no/<emp_no>', methods=['GET'])
def search_by_emp_no(emp_no: str):
    """ Production implementation would have decorators, at the very least:

    @login_required

    Actual valid routes:

    http://localhost:5000/employees/search-by-emp-no/10399
    """

    return EmployeesManager().select_by_employee_number(int(emp_no)).as_dict()

@bp.route('/save', methods=['POST'])
def save():
    """ Production implementation would have decorators, at the very least:

    @login_required

    Actual valid routes:

    http://localhost:5000/employees/save
    """

    params = request.values.to_dict(True)
    return EmployeesManager().write_to_database(params).as_dict()

@bp.route('/new', methods=['GET'])
def new():
    """ Production implementation would have decorators, at the very least:

    @login_required

    Actual valid routes:

    http://localhost:5000/employees/new
    """

    return make_response(render_template('admin/emp_edit.html'))

@bp.route('/', methods=['GET', 'POST'])
def search_form():
    """ Production implementation would have decorators, at the very least:

    @login_required

    Actual valid routes:

    http://localhost:5000/employees
    """    
    return render_template('admin/emp_search.html')

"""
App entry point.
"""

from flaskr import create_app

from flaskr.controllers.employees_admin import search_form

app = create_app()

@app.route("/")
def index():
    return search_form()

<!-- 30/04/2024. -->

# Both Examples Require Python 3.12.4

Please note, while the package itself does require Python 3.12.4, both examples do.

To install Python 3.12.4, please refer to the following post: [Installing Python 3.12.4 as an Additional Interpreter on Ubuntu 22.10 and Windows 10](https://behainguyen.wordpress.com/2024/06/28/installing-python-3-12-4-as-an-additional-interpreter-on-ubuntu-22-10-and-windows-10/).

# Further Information

🚀 A more detail version of this content can be found at 
[Python: A SQLAlchemy Wrapper Component That Works With Both Flask and FastAPI Frameworks](https://behainguyen.wordpress.com/2024/05/04/python-a-sqlalchemy-wrapper-component-that-works-with-both-flask-and-fastapi-frameworks/).

Note, the codes of [Flask example](https://github.com/behai-nguyen/bh_database/tree/main/examples/flaskr) and [FastAPI example](https://github.com/behai-nguyen/bh_database/tree/main/examples/fastapir) are essentially identical in the following areas:

* ``/models``
* ``/business``

In fact the codes in these two can be shared across to examples, but that would 
make the examples hard to follow.

* ``/controllers`` code is framework-dependent, so understandably, they are different.

For tests:

* ``/tests/unit``
* ``/tests/business``

are identical between the two examples.

* ``/tests/integration`` has only a single difference:

    * ``Flask``: ``response.get_data(as_text=True)``
    * ``FastAPI``: ``response.text``

* Module ``/tests/conftest.py`` is framework-dependent. Both modules return the same
  fixtures, but the codes are completely different.

* ``/templates/base.html`` has one difference:

    * ``Flask``: ``<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">``
    * ``FastAPI``: ``<link rel="stylesheet" href="{{ url_for('static', path='/styles.css') }}">``

The rest of the code, which is about application creation and instantiation, 
and so are framework-dependent, and are inevitably different.

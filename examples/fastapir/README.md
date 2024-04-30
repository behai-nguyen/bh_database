
This example seeks to demonstrate how the [bh-database](https://pypi.org/project/bh-database/) library can be used with the [FastAPI](https://fastapi.tiangolo.com/learn/) framework to perform CRUD operations generically.

This example demonstrates both MySQL and PostgreSQL.

# The Focus of this Example

The focus of this example should be the module [employees_mgr.py](https://github.com/behai-nguyen/bh_database/blob/70d67f5ec8aa8fc685ba5ad1648a83589d9bc733/examples/fastapir/src/fastapir/business/employees_mgr.py).

This module acts as a middle-man between the controller ([employees_mgr.py](https://github.com/behai-nguyen/bh_database/blob/70d67f5ec8aa8fc685ba5ad1648a83589d9bc733/examples/fastapir/src/fastapir/controllers/employees_admin.py)), and the model ([employees.py](https://github.com/behai-nguyen/bh_database/blob/70d67f5ec8aa8fc685ba5ad1648a83589d9bc733/examples/fastapir/src/fastapir/models/employees.py)).

It receives the request data from the controller, validate submitted data, then finally perform CRUD on this submitted and validated data.

Querying database is model-specific. Models must implement their own querying methods, and middle-men and controllers call those methods as appropriate.

``Insert`` and ``update`` operations are generic: models descend from [WriteCapableTable](https://bh-database.readthedocs.io/en/latest/base_table.html#bh_database.base_table.WriteCapableTable) inherit the [write_to_database](https://bh-database.readthedocs.io/en/latest/base_table.html#bh_database.base_table.WriteCapableTable.write_to_database) method.

Please pay attention to:

● The template function [write_to_database](https://github.com/behai-nguyen/bh_database/blob/70d67f5ec8aa8fc685ba5ad1648a83589d9bc733/examples/fastapir/src/fastapir/business/base_business.py#L314), in the module ``base_business.py``.

● The override method [_preprocess_write_data](https://github.com/behai-nguyen/bh_database/blob/70d67f5ec8aa8fc685ba5ad1648a83589d9bc733/examples/fastapir/src/fastapir/business/employees_mgr.py#L87), in the module ``employees_mgr.py``, in particular, the line:

```python
self.__employee_data[BH_REC_STATUS_FIELDNAME] = self._get_rec_status('empNo')
```

● The override method [_write](https://github.com/behai-nguyen/bh_database/blob/70d67f5ec8aa8fc685ba5ad1648a83589d9bc733/examples/fastapir/src/fastapir/business/employees_mgr.py#L128), in the module ``employees_mgr.py``, in particular, the line:

```python
status = employee.write_to_database([self.__employee_data])
```

# The Database

The ``employees`` MySQL database used is the [Oracle Corporation MySQL test database](https://github.com/datacharmer/test_db).

It is the same database used in the 70d67f5ec8aa8fc685ba5ad1648a83589d9bc733 [bh-database tests](https://github.com/behai-nguyen/bh_database/tree/70d67f5ec8aa8fc685ba5ad1648a83589d9bc733/tests).

Note, the``get_employees`` stored procedure / method is also required as per in the tests.

The PostgreSQL version of this test database was created using the [dimitri/pgloader](https://hub.docker.com/r/dimitri/pgloader/) migration tool.

I have discussed this migration process in the article 
[pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL](
https://behainguyen.wordpress.com/2022/11/13/pgloader-docker-migrating-from-docker-localhost-mysql-to-localhost-postgresql/).

# Switching Between MySQL and PostgreSQL

In the [.env](https://github.com/behai-nguyen/bh_database/blob/e86964c9a17b856e91ff6306593a503bcaffd3ee/examples/fastapir/.env) file, enable appropriate database URI.


**MySQL** -- enable this line:

```
SQLALCHEMY_DATABASE_URI = mysql+mysqlconnector://root:pcb.2176310315865259@localhost:3306/employees
```

**PostgreSQL** -- enable this line:

```
SQLALCHEMY_DATABASE_URI = postgresql+psycopg2://postgres:pcb.2176310315865259@localhost/employees
```

# JavaScripts Used In The Example

They are in this [this repo](https://github.com/behai-nguyen/js).

# Set Up and Run

Create the virtual environment ``venv``, specify the absolute path for ``virtualenv`` if there are multiple Python versions installed:

```
virtualenv venv
```

Activate the virtual environment ``venv``:

```
▶️Windows 10: \<path>\venv\Scripts\activate
▶️Ubuntu 22.10: /<path>/venv/bin/activate
```

Editable install run-time packages:

```
▶️Windows 10: \<path>\venv\Scripts\pip.exe install -e .
▶️Ubuntu 22.10: /<path>/venv/bin/pip install -e .
```

Editable install development packages:

```
▶️Windows 10: \<path>\venv\Scripts\pip.exe install -e .[dev]
▶️Ubuntu 22.10: /<path>/venv/bin/pip install -e .[dev]
```

Run (all) the tests:

```
▶️Windows 10: \<path>\venv\Scripts\pytest.exe
▶️Ubuntu 22.10: /<path>/venv/bin/pytest
```

Run the example proper development server:

```
▶️Windows 10: \<path>\venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 5000
▶️Ubuntu 22.10: /<path>/venv/bin/uvicorn main:app --host 0.0.0.0 --port 5000
```

Run the web UI:

```
http://localhost:5000
```

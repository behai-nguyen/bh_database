Base Table test modules
-----------------------

In addition to test modules listed in :ref:`core-test-modules`, the following model (table) 
oriented modules demonstrate how applications should subclass and use the methods in place to 
do database works:

.. line-block::

    ./tests/test_25_base_table_crud_methods_postgresql.py
    ./tests/test_26_base_table_crud_methods_mysql.py
    ./tests/test_30_base_table_exception_postgresql.py
    ./tests/test_31_base_table_exception_mysql.py

These test modules, together with fixtures defined in ``./tests/conftest.py``
should illustrate how the classes in this core module should work together.
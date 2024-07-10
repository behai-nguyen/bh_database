Core Module
===========

.. automodule:: bh_database.core
   :members:
   :undoc-members:
   :show-inheritance:

.. _core-test-modules:

Core Test Modules
-----------------

There are following modules:

.. line-block::
   
   ./tests/test_01_core_database_postgresql.py
   ./tests/test_02_core_database_mysql.py
   ./tests/test_05_core_basesqlalchemy_postgresql.py
   ./tests/test_06_core_basesqlalchemy_mysql.py
   ./tests/test_11_paginator_postgresql.py
   ./tests/test_12_paginator_mysql.py
   ./tests/test_15_base_table_postgresql.py
   ./tests/test_16_base_table_mysql.py
   ./tests/test_17_base_table_methods.py
   ./tests/test_20_base_table_dunder.py

These test modules, together with fixtures defined in ``./tests/conftest.py``
should illustrate how the classes in this core module should work together.
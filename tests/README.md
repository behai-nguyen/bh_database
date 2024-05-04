# The Test Database

The [``employees``](https://github.com/behai-nguyen/bh_database/blob/c1300d927f6db7806bb67ab43eefb94f66aa4a51/tests/__init__.py#L9) MySQL database used in the tests is the [Oracle Corporation MySQL test database](https://github.com/datacharmer/test_db).

The PostgreSQL version of this test database was created using the [dimitri/pgloader](https://hub.docker.com/r/dimitri/pgloader/) migration tool.

I have discussed this migration process in the article 
[pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL](
https://behainguyen.wordpress.com/2022/11/13/pgloader-docker-migrating-from-docker-localhost-mysql-to-localhost-postgresql/).

# The Test ``get_employees`` Stored Procedure / Method

Some of the tests will need to call the stored procedure / method ``get_employees``.

For MySQL, please apply this script [04_test_get_employees_stored_method.sql](https://github.com/behai-nguyen/bh_database/blob/main/sql_scripts/mysql/04_test_get_employees_stored_method.sql).

For PostgreSQL, please apply this script [04_test_get_employees_stored_method.sql](https://github.com/behai-nguyen/bh_database/blob/main/sql_scripts/postgres/04_test_get_employees_stored_method.sql).

Please see also [Getting Started – Please Read First | The test database](https://bh-database.readthedocs.io/en/latest/getting_started.html#the-test-database).

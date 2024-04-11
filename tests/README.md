# The Test Database

The [``employees``](https://github.com/behai-nguyen/bh_database/blob/c1300d927f6db7806bb67ab43eefb94f66aa4a51/tests/__init__.py#L9) MySQL database used in the tests is the [Oracle Corporation MySQL test database](https://github.com/datacharmer/test_db).

The PostgreSQL version of this test database was created using the [dimitri/pgloader](https://hub.docker.com/r/dimitri/pgloader/) migration tool.

I have discussed this migration process in the article 
[pgloader Docker: migrating from Docker & localhost MySQL to localhost PostgreSQL](
https://behainguyen.wordpress.com/2022/11/13/pgloader-docker-migrating-from-docker-localhost-mysql-to-localhost-postgresql/).

# The Test ``get_employees`` Stored Procedure / Method

Some of the tests will need to call the stored procedure / method ``get_employees``.

For MySQL, please apply this script [get_employees_mysql.sql](https://github.com/behai-nguyen/bh_database/blob/main/tests/stored_methods/get_employees_mysql.sql).

For PostgreSQL, please apply this script [get_employees_postgresql.sql](https://github.com/behai-nguyen/bh_database/blob/main/tests/stored_methods/get_employees_postgresql.sql).

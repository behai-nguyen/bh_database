"""
Generic constants and messages.
"""
#: Support only two database types: MySQL and PostgreSQL. See :py:doc:`core`.
BH_UNSUPPORTED_DATABASE_MSG = "{!r} unsupported database."
#: Write-pending records' status. See :meth:`write_to_database(self, data: list) -> ResultStatus \
#: <bh_database.base_table.WriteCapableTable.write_to_database>`.
BH_REC_STATUS_FIELDNAME = "recStatus"
#: Write-pending ``new`` records -- these records are to be inserted. See \
#: :meth:`write_to_database(self, data: list) -> ResultStatus \
#: <bh_database.base_table.WriteCapableTable.write_to_database>`.
BH_RECORD_STATUS_NEW = "new"
#: Write-pending ``modified`` records -- these records are to be updated. See \
#: :meth:`write_to_database(self, data: list) -> ResultStatus \
#: <bh_database.base_table.WriteCapableTable.write_to_database>`.
BH_RECORD_STATUS_MODIFIED = "modified"
#: Write-pending ``unchanged`` records. Not used.
BH_RECORD_STATUS_UNCHANGED = "unchanged"

#: Failed to get a next unique integer value for a (primary key) column. 
BH_NEXT_ID_NO_RESULT_MSG = "Get next Id for {0}.{1} failed to get next value."
#: A stored procedure returns no data based on input parameters. See \
#: :meth:`run_stored_proc(self, stored_proc_name: str, params: list, auto_session=False) -> dict: \
#: <bh_database.base_table.WriteCapableTable.run_stored_proc>`.
BH_STORED_PROC_NO_RESULT_SET_MSG = "Stored proc {}(...) appears to return no resultset."
#: A full text SELECT SQL statement returns no data. See \
#: :meth:`run_select_sql(self, sql: str, auto_session=False) -> dict:
#: <bh_database.base_table.ReadOnlyTable.run_select_sql>`.
BH_SQL_NO_DATA_MSG = "No data for the selection criteria."

#: A full text SELECT SQL statement returns some data. See \
#: :meth:`run_select_sql(self, sql: str, auto_session=False) -> dict:
#: <bh_database.base_table.ReadOnlyTable.run_select_sql>`.
BH_RETRIEVED_SUCCESSFUL_MSG = "Data has been retrieved successfully."
#: Pending data have been successfully written to the database. See \
#: :meth:`write_to_database(self, data: list) -> ResultStatus \
#: <bh_database.base_table.WriteCapableTable.write_to_database>`.
BH_SAVED_SUCCESSFUL_MSG = "Data has been saved successfully."
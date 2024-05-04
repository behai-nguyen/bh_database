delete from unique_id where tablename = 'employees';

insert into unique_id (tablename, columnname, id)
    select 'employees', 'emp_no', max(emp_no)+1 from employees;

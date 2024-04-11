/*
    To test:
	
    select * from get_employees('%nas%', '%AN');
*/
create or replace function get_employees( 
    pmLastName varchar(16), 
    pmFirstName varchar(14) 
)
returns table ( 
    emp_no integer,
    birth_date date,
    first_name varchar(14),
    last_name varchar(16),
    gender character(1),
    hire_date date 
)
language plpgsql
as $$
begin
  return query
  select * from employees e where (lower(e.last_name) like lower(pmLastName))
    and (lower(e.first_name) like lower(pmFirstName)) order by e.emp_no;
end;
$$
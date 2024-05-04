/*
    Description: Get the next unique integer Id based on a 
       table name and a column name.
	   
    To drop: 

    drop function if exists get_unique_id;
   
    To call ( tests ):
	
    select get_unique_id('employees', 'emp_no');
*/

delimiter //

drop function if exists get_unique_id; //

create function get_unique_id(PM_TABLENAME varchar(64), PM_COLUMNNAME varchar(64)) returns int
begin
  declare LocalID int;

  select
    id
  into
    LocalID
  from
    unique_id
  where 
    (tablename = PM_TABLENAME)
    and (columnname = PM_COLUMNNAME);

  if isnull(LocalID) then #1
    set LocalID = 1;

    insert into unique_id
    (
      tablename,
      columnname,
      id
    )
    values
    (
      PM_TABLENAME,
      PM_COLUMNNAME,
      LocalID + 1
    );

  else
    update
      unique_id
    set
      id = LocalID + 1
    where
      (tablename = PM_TABLENAME)
      and (columnname = PM_COLUMNNAME);
  end if; #1

  return LocalID;
end; //

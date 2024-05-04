/*
    Description: Get the next unique integer Id based on a 
       table name and a column name.

    To drop: 

    drop function get_unique_id(varchar,varchar);

    To call ( tests ):

    select get_unique_id('client', 'client_id') id;
*/

create or replace function get_unique_id( pmTableName varchar(64), pmColumnName varchar(64) ) 
returns int
language plpgsql
as
$$
declare 
    LocalId int;
begin
  select 
    ID into LocalId
  from
    unique_id
  where
    ( tablename = pmTableName ) and ( columnname = pmColumnName );
	
  if LocalId is null then
    LocalId := 1;
	
    insert into unique_id ( tablename, columnname, ID )
    values ( pmTableName, pmColumnName, LocalId + 1 );
	
  else	
  
    update unique_id set ID = LocalId + 1
    where ( tablename = pmTableName ) and ( columnname = pmColumnName );
  end if;

  return LocalId;
end;
$$
/*
    To test:
	
    call get_employees('%nas%', '%AN');
*/

DROP PROCEDURE IF EXISTS get_employees;

DELIMITER $$
CREATE DEFINER=`root`@`%` PROCEDURE `get_employees`( pmLastName varchar(16), pmFirstName varchar(14) )
    READS SQL DATA
begin
  select * from employees e where (e.last_name like pmLastName)
    and (e.first_name like pmFirstName) order by e.emp_no;
end$$
DELIMITER ;
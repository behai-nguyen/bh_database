"""
Implement some validation for the employees data.
"""

from wtforms import (    
    StringField,
    DateField,
)

from wtforms.validators import (
    InputRequired,
    Length,
    AnyOf,
)

from .base_validation import BaseValidationForm

PARTIAL_LAST_NAME_MSG = "Please provide partial search last name between 1 and 16 characters, must include wildcard %. E.g. %nas%"
PARTIAL_FIRST_NAME_MSG = "Please provide partial search first name between 1 and 14 characters, must include wildcard %. E.g. %An"
BIRTH_DATE_MSG = "For birth date, please enter a date in format dd/mm/yyyy. E.g. 25/2/1999"
LAST_NAME_MSG = "For last name, please enter between 1 and 16 characters"
FIRST_NAME_MSG = "For first name, please enter between 1 and 14 characters"
GENDER_MSG = 'Please select a gender'
HIRE_DATE_MSG = "For hire date, please enter a date in format dd/mm/yyyy. E.g. 25/2/2011"
HIRE_DATE_AFTER_BIRTH_DATE_MSG = 'Hire Date must be after Birth Date'

class SearchByNameForm(BaseValidationForm):
    last_name = StringField('Partial Last Name', validators=[InputRequired(PARTIAL_LAST_NAME_MSG),
                                Length(1, 16, PARTIAL_LAST_NAME_MSG)])
    
    first_name = StringField('Partial First Name', validators=[InputRequired(PARTIAL_FIRST_NAME_MSG),
                                Length(1, 14, PARTIAL_FIRST_NAME_MSG)])

    # Custom validation function.
    def validate(self, extra_validators=None):
        res = super().validate(extra_validators)
        if res:
            if self.last_name.data.find("%") == -1:
                self.last_name.errors.append(PARTIAL_LAST_NAME_MSG)
                res = False
            
            if self.first_name.data.find("%") == -1:
                self.first_name.errors.append(PARTIAL_FIRST_NAME_MSG)
                res = False

            return res
        return False
    
class EditorForm(BaseValidationForm): 
    # emp_no is not always available at the time of validation: for a new employee, 
    # nothing has been written onto the database yet. employees.emp_no is only 
    # available after an employee has been written.
    # 
    # emp_no
    birth_date = DateField('Birth Date', validators=[InputRequired(BIRTH_DATE_MSG)], format='%d/%m/%Y')
    first_name = StringField('First Name', validators=[InputRequired(FIRST_NAME_MSG),
                                Length(1, 14, FIRST_NAME_MSG)])
    last_name = StringField('Last Name', validators=[InputRequired(LAST_NAME_MSG),
                                Length(1, 16, LAST_NAME_MSG)])
    gender = StringField('Gender', validators=[InputRequired(GENDER_MSG), 
                                 AnyOf(['F', 'M'], GENDER_MSG)])
    hire_date = DateField('Hire Date', validators=[InputRequired(HIRE_DATE_MSG)], format='%d/%m/%Y')

    # Custom validation function.
    def validate(self, extra_validators=None):
        res = super().validate(extra_validators)
        if res:
            # We could do more valiations, such as how many years apart, etc.
            # But for the purpose of this example, we will just keep it simple.
            if self.hire_date.data <= self.birth_date.data:
                self.hire_date.errors.append(HIRE_DATE_AFTER_BIRTH_DATE_MSG)
                return False

            return True
        return False

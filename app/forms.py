from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField, SubmitField)
from wtforms.validators import DataRequired

v = [DataRequired()]


class EmployeeLoginForm(FlaskForm):
    employee_number = StringField('employee number', v)
    password = PasswordField('password', v)
    submit = SubmitField('Login')

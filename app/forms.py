from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, PasswordField, SubmitField, SelectField)
from wtforms.validators import DataRequired

v = [DataRequired()]


class EmployeeLoginForm(FlaskForm):
    employee_number = StringField('employee number', v)
    password = PasswordField('password', v)
    submit = SubmitField('Login')


class TableAssignmentForm(FlaskForm):
    tables = SelectField("Tables", v, coerce=int)
    servers = SelectField('Servers', v, coerce=int)
    assign = SubmitField("Assign")

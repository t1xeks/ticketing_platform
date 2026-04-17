from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class IssueFormEmployee(FlaskForm):
    category = SelectField(
        "Category",
        choices=[
            ("Hardware", "Hardware"),
            ("Software", "Software"),
            ("Network", "Network"),
            ("Printing", "Printing"),
            ("Other", "Other"),
        ],
        validators=[DataRequired()],
    )
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Submit")


class IssueFormSupport(FlaskForm):
    status = SelectField(
        "Status",
        choices=[("Reported", "Reported"), ("In Progress", "In Progress"), ("Resolved", "Resolved")],
        default="In Progress",
    )
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    employee_id = IntegerField("Employee ID", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("New Password", validators=[Optional()])
    confirm_password = PasswordField("Confirm New Password", validators=[EqualTo("password", message="Passwords must match")])
    submit = SubmitField("Update")
    delete = SubmitField("Delete Account")

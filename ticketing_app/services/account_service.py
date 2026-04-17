from werkzeug.security import generate_password_hash

from ticketing_app.exceptions import ValidationError
from ticketing_app.extensions import db
from ticketing_app.models import Employee, Issue, SupportStaff, User


class AccountService:
    @staticmethod
    def update_account(user, user_type, new_email, new_password=None):
        user_with_same_email = User.query.filter_by(email=new_email).first()
        if user_with_same_email and user_with_same_email.id != user.id:
            raise ValidationError("Email is already in use.")

        old_email = user.email
        user.email = new_email
        if new_password:
            user.password = generate_password_hash(new_password, method="sha256")

        if user_type == "employee":
            employee = Employee.query.filter_by(email=old_email).first()
            if employee:
                employee.email = new_email
            issues = Issue.query.filter_by(employee_email=old_email).all()
            for issue in issues:
                issue.employee_email = new_email
        elif user_type == "support":
            support = SupportStaff.query.filter_by(email=old_email).first()
            if support:
                support.email = new_email

        db.session.commit()

    @staticmethod
    def delete_account(user, user_type):
        if user_type == "employee":
            employee = Employee.query.filter_by(email=user.email).first()
            if employee:
                db.session.delete(employee)
        db.session.delete(user)
        db.session.commit()

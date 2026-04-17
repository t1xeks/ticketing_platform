from werkzeug.security import check_password_hash, generate_password_hash

from ticketing_app.exceptions import ValidationError
from ticketing_app.extensions import db
from ticketing_app.models import Employee, SupportStaff, User


class AuthService:
    @staticmethod
    def get_user_type(email):
        if Employee.query.filter_by(email=email).first():
            return "employee"
        if SupportStaff.query.filter_by(email=email).first():
            return "support"
        return None

    @staticmethod
    def register_employee(data):
        employee_by_id = Employee.query.filter_by(employee_id=data["employee_id"]).first()
        if employee_by_id:
            raise ValidationError("Employee ID already exists.")

        email_taken = Employee.query.filter_by(email=data["email"]).first() or SupportStaff.query.filter_by(email=data["email"]).first()
        if email_taken:
            raise ValidationError("Email already exists.")

        user = User(email=data["email"], password=generate_password_hash(data["password"], method="sha256"))
        employee = Employee(
            employee_id=data["employee_id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            location=data["location"],
        )
        db.session.add(user)
        db.session.add(employee)
        db.session.commit()
        return user

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return user
        return None

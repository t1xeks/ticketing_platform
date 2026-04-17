from ticketing_app.extensions import db


class Employee(db.Model):
    __tablename__ = "employees"

    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    issues = db.relationship("Issue", backref="employee", lazy=True, cascade="all, delete-orphan")

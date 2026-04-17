from ticketing_app.extensions import db


class SupportStaff(db.Model):
    __tablename__ = "support_staff"

    support_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

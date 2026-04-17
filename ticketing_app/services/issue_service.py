import random

from ticketing_app.exceptions import AuthorizationError, NotFoundError, ValidationError
from ticketing_app.extensions import db
from ticketing_app.models import Employee, Issue, SupportStaff


class IssueService:
    @staticmethod
    def list_issues_for_user(email, user_type):
        if user_type == "support":
            return Issue.query.all()
        if user_type == "employee":
            return Issue.query.filter_by(employee_email=email).all()
        raise AuthorizationError("Unknown user role.")

    @staticmethod
    def get_issue_or_404(issue_id):
        issue = Issue.query.get(issue_id)
        if issue is None:
            raise NotFoundError("Issue not found.")
        return issue

    @staticmethod
    def ensure_access(issue, email, user_type):
        if issue.employee_email != email and user_type != "support":
            raise AuthorizationError("You are not allowed to access this issue.")

    @staticmethod
    def create_issue(employee_email, category, description):
        employee = Employee.query.filter_by(email=employee_email).first()
        if not employee:
            raise ValidationError("Employee profile was not found.")

        support_names = [row.name for row in SupportStaff.query.with_entities(SupportStaff.name).all()]
        if not support_names:
            raise ValidationError("No support staff available for assignment.")

        issue = Issue(
            employee_id=employee.employee_id,
            employee_name=employee.name,
            employee_email=employee.email,
            location=employee.location,
            category=category,
            description=description,
            support_name=random.choice(support_names),
        )
        db.session.add(issue)
        db.session.commit()
        return issue

    @staticmethod
    def update_issue_by_role(issue, user_type, current_email, payload):
        if user_type == "employee":
            issue.category = payload["category"]
            issue.description = payload["description"]
        elif user_type == "support":
            support_user = SupportStaff.query.filter_by(email=current_email).first()
            if not support_user:
                raise AuthorizationError("Support profile not found.")
            issue.status = payload["status"]
            issue.support_name = support_user.name
        else:
            raise AuthorizationError("Unknown user role.")

        db.session.commit()
        return issue

    @staticmethod
    def delete_issue(issue, current_email):
        if issue.employee_email != current_email:
            raise AuthorizationError("Only the issue owner can delete it.")
        db.session.delete(issue)
        db.session.commit()

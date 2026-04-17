from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from ticketing_app.exceptions import AuthorizationError, ValidationError
from ticketing_app.services import AuthService, IssueService

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _issue_to_dict(issue):
    return {
        "issue_id": issue.issue_id,
        "employee_id": issue.employee_id,
        "employee_name": issue.employee_name,
        "employee_email": issue.employee_email,
        "location": issue.location,
        "category": issue.category,
        "description": issue.description,
        "status": issue.status,
        "support_name": issue.support_name,
    }


@api_bp.get("/issues")
@login_required
def list_issues():
    """List issues for current user.
    ---
    tags: [Issues]
    responses:
      200:
        description: Issues returned successfully
    """
    user_type = AuthService.get_user_type(current_user.email)
    issues = IssueService.list_issues_for_user(current_user.email, user_type)
    return jsonify([_issue_to_dict(issue) for issue in issues])


@api_bp.post("/issues")
@login_required
def create_issue():
    """Create a new issue (employee only).
    ---
    tags: [Issues]
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [category, description]
          properties:
            category:
              type: string
            description:
              type: string
    responses:
      201:
        description: Issue created
    """
    user_type = AuthService.get_user_type(current_user.email)
    if user_type != "employee":
        raise AuthorizationError("Only employees can create issues.")

    data = request.get_json(silent=True) or {}
    category = data.get("category")
    description = data.get("description")
    if not category or not description:
        raise ValidationError("category and description are required.")
    issue = IssueService.create_issue(current_user.email, category, description)
    return jsonify(_issue_to_dict(issue)), 201


@api_bp.patch("/issues/<int:issue_id>")
@login_required
def update_issue(issue_id):
    """Update issue by role.
    ---
    tags: [Issues]
    parameters:
      - in: path
        name: issue_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            category:
              type: string
            description:
              type: string
            status:
              type: string
    responses:
      200:
        description: Issue updated
    """
    issue = IssueService.get_issue_or_404(issue_id)
    user_type = AuthService.get_user_type(current_user.email)
    IssueService.ensure_access(issue, current_user.email, user_type)

    payload = request.get_json(silent=True) or {}
    if user_type == "employee":
        if not payload.get("category") or not payload.get("description"):
            raise ValidationError("category and description are required for employee update.")
        data = {"category": payload["category"], "description": payload["description"]}
    else:
        if not payload.get("status"):
            raise ValidationError("status is required for support update.")
        data = {"status": payload["status"]}

    updated = IssueService.update_issue_by_role(issue, user_type, current_user.email, data)
    return jsonify(_issue_to_dict(updated))


@api_bp.delete("/issues/<int:issue_id>")
@login_required
def delete_issue(issue_id):
    """Delete issue by owner.
    ---
    tags: [Issues]
    parameters:
      - in: path
        name: issue_id
        type: integer
        required: true
    responses:
      200:
        description: Issue deleted
    """
    issue = IssueService.get_issue_or_404(issue_id)
    IssueService.delete_issue(issue, current_user.email)
    return jsonify({"message": "Issue deleted"})

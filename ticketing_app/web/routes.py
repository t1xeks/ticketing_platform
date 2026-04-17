from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ticketing_app.exceptions import ValidationError
from ticketing_app.forms import IssueFormEmployee, IssueFormSupport, LoginForm, RegistrationForm, UpdateAccountForm
from ticketing_app.services import AccountService, AuthService, IssueService

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
@login_required
def home():
    user_type = AuthService.get_user_type(current_user.email)
    return render_template("home.html", user_type=user_type)


@web_bp.route("/issues")
@login_required
def all_issues():
    user_type = AuthService.get_user_type(current_user.email)
    if user_type != "support":
        flash("You do not have the necessary permissions to view this page.", "danger")
        return redirect(url_for("web.home"))
    issues = IssueService.list_issues_for_user(current_user.email, user_type)
    return render_template("issues.html", issues=issues, user_type=user_type)


@web_bp.route("/my_issues")
@login_required
def my_issues():
    user_type = AuthService.get_user_type(current_user.email)
    if user_type != "employee":
        flash("Only employees can access this page.", "danger")
        return redirect(url_for("web.home"))
    issues = IssueService.list_issues_for_user(current_user.email, user_type)
    return render_template("issues.html", issues=issues, user_type=user_type)


@web_bp.route("/issues/<int:issue_id>", methods=["GET"])
@login_required
def issue(issue_id):
    issue_obj = IssueService.get_issue_or_404(issue_id)
    user_type = AuthService.get_user_type(current_user.email)
    IssueService.ensure_access(issue_obj, current_user.email, user_type)
    return render_template("issue.html", issue=issue_obj, user_type=user_type)


@web_bp.route("/issue/new", methods=["GET", "POST"])
@login_required
def add_issue():
    user_type = AuthService.get_user_type(current_user.email)
    form = IssueFormEmployee()
    if user_type != "employee":
        flash("Only employees can create issues.", "danger")
        return redirect(url_for("web.home"))
    if form.validate_on_submit():
        try:
            issue_obj = IssueService.create_issue(current_user.email, form.category.data, form.description.data)
            return redirect(url_for("web.issue", issue_id=issue_obj.issue_id))
        except ValidationError as error:
            flash(error.message, "danger")
    return render_template("add_issue.html", title="New Issue", form=form, user_type=user_type)


@web_bp.route("/issue/<int:issue_id>/update", methods=["GET", "POST"])
@login_required
def update_issue(issue_id):
    issue_obj = IssueService.get_issue_or_404(issue_id)
    user_type = AuthService.get_user_type(current_user.email)
    IssueService.ensure_access(issue_obj, current_user.email, user_type)

    form = IssueFormEmployee() if user_type == "employee" else IssueFormSupport()
    if form.validate_on_submit():
        payload = (
            {"category": form.category.data, "description": form.description.data}
            if user_type == "employee"
            else {"status": form.status.data}
        )
        IssueService.update_issue_by_role(issue_obj, user_type, current_user.email, payload)
        flash("Issue has been updated!", "success")
        return redirect(url_for("web.issue", issue_id=issue_obj.issue_id))

    if request.method == "GET":
        if user_type == "employee":
            form.category.data = issue_obj.category
            form.description.data = issue_obj.description
        else:
            form.status.data = issue_obj.status
    return render_template("update_issue.html", title="Update Issue", form=form, user_type=user_type)


@web_bp.route("/issue/<int:issue_id>/delete", methods=["POST"])
@login_required
def delete_issue(issue_id):
    issue_obj = IssueService.get_issue_or_404(issue_id)
    IssueService.delete_issue(issue_obj, current_user.email)
    flash("Your issue has been deleted!", "success")
    return redirect(url_for("web.my_issues"))


@web_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("web.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            AuthService.register_employee(
                {
                    "employee_id": form.employee_id.data,
                    "name": form.name.data,
                    "email": form.email.data,
                    "phone": form.phone.data,
                    "location": form.location.data,
                    "password": form.password.data,
                }
            )
            flash("Your account has been created! You can now log in.", "success")
            return redirect(url_for("web.login"))
        except ValidationError as error:
            flash(error.message, "danger")
    return render_template("register.html", title="Register", form=form)


@web_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        user_type = AuthService.get_user_type(current_user.email)
        return redirect(url_for("web.all_issues" if user_type == "support" else "web.my_issues"))
    form = LoginForm()
    if form.validate_on_submit():
        user = AuthService.authenticate(form.email.data, form.password.data)
        if user:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            user_type = AuthService.get_user_type(user.email)
            fallback = "web.all_issues" if user_type == "support" else "web.my_issues"
            return redirect(next_page) if next_page else redirect(url_for(fallback))
        flash("Login unsuccessful. Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@web_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    user_type = AuthService.get_user_type(current_user.email)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        action = request.form.get("action")
        if action == "delete":
            AccountService.delete_account(current_user, user_type)
            flash("Your account has been deleted.", "success")
            return redirect(url_for("web.login"))
        if action == "update":
            try:
                AccountService.update_account(current_user, user_type, form.email.data, form.password.data)
                flash("Your account has been updated!", "success")
            except ValidationError as error:
                flash(error.message, "danger")
            return redirect(url_for("web.account"))
    elif request.method == "GET":
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form=form, user_type=user_type)


@web_bp.route("/about")
@login_required
def about():
    user_type = AuthService.get_user_type(current_user.email)
    return render_template("about.html", user_type=user_type)


@web_bp.route("/client")
@login_required
def client_page():
    return render_template("client.html", user_type=AuthService.get_user_type(current_user.email))


@web_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("web.login"))

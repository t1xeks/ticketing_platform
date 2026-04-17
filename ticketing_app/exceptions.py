from flask import jsonify, render_template, request


class AppError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


class NotFoundError(AppError):
    status_code = 404


class AuthorizationError(AppError):
    status_code = 403


class ValidationError(AppError):
    status_code = 422


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": error.message}), error.status_code
        return render_template("error.html", message=error.message, code=error.status_code), error.status_code

    @app.errorhandler(403)
    def handle_forbidden(_error):
        message = "You do not have permission to access this page."
        if request.path.startswith("/api/"):
            return jsonify({"error": message}), 403
        return render_template("error.html", message=message, code=403), 403

    @app.errorhandler(404)
    def handle_not_found(_error):
        message = "The requested page was not found."
        if request.path.startswith("/api/"):
            return jsonify({"error": message}), 404
        return render_template("error.html", message=message, code=404), 404

    @app.errorhandler(500)
    def handle_internal(_error):
        message = "Internal server error."
        if request.path.startswith("/api/"):
            return jsonify({"error": message}), 500
        return render_template("error.html", message=message, code=500), 500

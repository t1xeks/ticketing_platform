from flask import Flask
from werkzeug.security import generate_password_hash

from ticketing_app.api.routes import api_bp
from ticketing_app.config import Config
from ticketing_app.exceptions import register_error_handlers
from ticketing_app.extensions import csrf, db, login_manager, swagger
from ticketing_app.models import SupportStaff, User
from ticketing_app.web.routes import web_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    swagger.init_app(
        app,
        config={
            "headers": [],
            "specs": [{"endpoint": "apispec_1", "route": "/apispec_1.json", "rule_filter": lambda rule: True, "model_filter": lambda tag: True}],
            "swagger_ui": True,
            "specs_route": "/api/docs/",
        },
    )
    login_manager.login_view = "web.login"

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    register_error_handlers(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        admin_user = User.query.filter_by(email="admin@email.com").first()
        admin_support = SupportStaff.query.filter_by(email="admin@email.com").first()
        if admin_user is None:
            admin_user = User(email="admin@email.com", password=generate_password_hash("qwer1234"))
            db.session.add(admin_user)
        if admin_support is None:
            admin_support = SupportStaff(name="Admin", email="admin@email.com")
            db.session.add(admin_support)
        db.session.commit()

    return app

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flasgger import Swagger

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
swagger = Swagger()

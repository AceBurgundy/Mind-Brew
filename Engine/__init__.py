from re import template
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from Engine.config import Config

login_manager = LoginManager()
login_manager.login_view = 'app-user.login'

db = SQLAlchemy()
main_admin = Admin(template_mode='bootstrap3')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    login_manager.init_app(app)
    db.init_app(app)
    main_admin.init_app(app)

    from Engine.user.routes import user
    from Engine.review.routes import review
    from Engine.index.routes import index
    from Engine.admin.routes import author
    from Engine.errors.handlers import errors

    app.register_blueprint(user)
    app.register_blueprint(review)
    app.register_blueprint(index)
    app.register_blueprint(author)
    app.register_blueprint(errors)

    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    app.after_request

    return app

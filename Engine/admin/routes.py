from flask import Blueprint
from Engine import main_admin, db
from Engine.models import User, Subject, Reviewer
from flask_admin.contrib.sqla import ModelView

author = Blueprint('author', __name__,
                   template_folder='templates/admin', static_folder='static/admin')
main_admin.add_view(ModelView(User, db.session))
main_admin.add_view(ModelView(Subject, db.session))
main_admin.add_view(ModelView(Reviewer, db.session))

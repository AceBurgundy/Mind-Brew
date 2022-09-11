from flask import Blueprint, redirect, url_for
from Engine import main_admin, db
from Engine.models import User, Subject, Reviewer, Notification, Message
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
import os

author = Blueprint('author', __name__,
                   template_folder='templates/admin', static_folder='static/admin')


class myModelView(ModelView):
    def is_accesible():
        if current_user == User.query.filter_by(username=os.getenv("ADMIN")).first() and current_user.is_authenticated:
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user.login'))


main_admin.add_view(myModelView(User, db.session))
main_admin.add_view(myModelView(Subject, db.session))
main_admin.add_view(myModelView(Reviewer, db.session))
main_admin.add_view(myModelView(Notification, db.session))
main_admin.add_view(myModelView(Message, db.session))

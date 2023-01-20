from flask import Blueprint, redirect, request, url_for
from Engine import main_admin, db
from Engine.models import Message, User, Reviewer, Question, Subject, Choice, Answer
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
import os

author = Blueprint('author', __name__,
                   template_folder='templates/admin', static_folder='static/admin')


class myModelView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated and current_user == User.query.filter_by(username=os.getenv("ADMIN")).first():
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('app-user.login'))


main_admin.add_view(myModelView(User, db.session))
main_admin.add_view(myModelView(Message, db.session))
main_admin.add_view(myModelView(Reviewer, db.session))
main_admin.add_view(myModelView(Subject, db.session))
main_admin.add_view(myModelView(Question, db.session))
main_admin.add_view(myModelView(Choice, db.session))
main_admin.add_view(myModelView(Answer, db.session))

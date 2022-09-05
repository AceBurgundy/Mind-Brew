from datetime import datetime
from Engine import db, login_manager
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView

"""
The function below is a callback used to reload the user object from the user ID stored in the session.
It should take the str ID of a user, and return the corresponding user object. For example:
"""


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(120), unique=True, nullable=False)
    school = db.Column(db.String(300))
    course = db.Column(db.String(60))
    phone = db.Column(db.String(15))
    profile_picture = db.Column(
        db.String(100), nullable=False, default='default.jpg')
    password = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime(), default=datetime.now)
    last_online = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now)

    # # this is not a column so we wont see a projects column in the User database. Instead,
    # # it runs a additional querry in the backrground to match the projects that the user has created

    def __repr__(self):
        return f"User('{self.username}') "


class Subject(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    creation_date = db.Column(db.DateTime(), default=datetime.now)
    professor = db.Column(db.String(80))
    image = db.Column(
        db.String(100), nullable=False, default='subject.jpg')
    score = db.Column(db.Integer, nullable=False, default=0)
    bought_test = db.Column(db.Boolean, nullable=False, default=False)
    # code = db.Column(db.String(40), nullable=False)

    questions = db.relationship('Reviewer', backref='subject', lazy=True)

    def __repr__(self):
        return f"Subject('{self.name}','{self.professor}','{self.bought_test}') "


class Reviewer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Text(nullable=False)
    choice_1 = db.Column(db.String(100), nullable=False)
    choice_2 = db.Column(db.String(100), nullable=False)
    choice_3 = db.Column(db.String(100), nullable=False)
    choice_4 = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey(
        'subject.id'), nullable=False)

    def __repr__(self):
        return f"Reviewer('{self.question}')"


class BufferAnswers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(100), nullable=False)
    reviwer_id = db.Column(db.Integer, db.ForeignKey(
        'reviewer.id'), nullable=False)

    def __repr__(self):
        return f"BufferAnswers('{self.answer}')"

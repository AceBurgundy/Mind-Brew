import json
from time import time
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


attempts = db.Table(
    db.Column("id", db.Integer, primary_key=True, nullable=False),
    db.Column("reviewer_id", db.Integer, db.ForeignKey(
        'reviewer.id'), nullable=False),
    db.Column("user_id", db.Integer, db.ForeignKey(
        'user.id'), nullable=False),
    db.Column("status", db.String(20), nullable=False),
    db.Column("score", db.Integer, nullable=False, default=0),
    db.Column("start_time", db.DateTime(),
              default=datetime.now, nullable=False),
    db.Column("end_time", db.DateTime(), default=datetime.now),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
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
    creation_date = db.Column(
        db.DateTime(), default=datetime.now, nullable=False)
    last_online = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)

    reviewers = db.relationship('Reviewer', backref='owned_by', lazy=True)

    messages = db.relationship(
        'Message', backref='received_messages', lazy=True)

    attempts = db.relationship(
        'Project', secondary=attempts, backref='taker')
    # # this is not a column so we wont see a projects column in the User database. Instead,
    # # it runs a additional querry in the backrground to match the projects that the user has created

    def __repr__(self):
        return f"User('{self.username}','{self.reviewers}','{self.messages}') "


class Message(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)
    recipient_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"Message('{self.sender_id}','{self.recipient_id}','{self.body}')"


class Reviewer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    creation_date = db.Column(
        db.DateTime(), default=datetime.now, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    availablility = db.Column(db.Boolean, nullable=False, default=True)
    students = db.Column(db.Integer, db.ForeignKey('user.id'))
    questions = db.relationship(
        'Question', backref='reviewer', lazy=True, passive_deletes=True)

    def __repr__(self):
        return f"Reviewer('{self.name}','{self.author}') "


class Question(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    creation_date = db.Column(
        db.DateTime(), default=datetime.now, nullable=False)
    updated_date = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)

    question = db.Column(db.String(1000), nullable=False)

    choices = db.relationship(
        'Choice', backref='question', lazy=True, passive_deletes=True)

    answers = db.relationship(
        'Choice', backref='question', lazy=True, uselist=False, passive_deletes=True)

    reviewer_id = db.Column(db.Integer, db.ForeignKey(
        'reviewer.id'), nullable=False, ondelete="CASCADE")

    def __repr__(self):
        return f"Question('{self.question}')"


class Choice(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    creation_date = db.Column(
        db.DateTime(), default=datetime.now, nullable=False)
    updated_date = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    choice = db.Column(db.String(100), nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False, ondelete="CASCADE")

    def __repr__(self):
        return f"Choice('{self.choice}')"


class Answer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    creation_date = db.Column(
        db.DateTime(), default=datetime.now, nullable=False)
    updated_date = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)

    answer = db.Column(db.String(100), nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False, ondelete="CASCADE")

    def __repr__(self):
        return f"Answer('{self.answer}')"

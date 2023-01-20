from datetime import datetime
from Engine import db, login_manager
from flask_login import UserMixin

"""
The function below is a callback used to reload the user object from the user ID stored in the session.
It should take the str ID of a user, and return the corresponding user object. For example:
"""


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


attempt_review = db.Table("attempt_review",
                          db.Column("id", db.Integer,
                                    primary_key=True, nullable=False),
                          db.Column("attempt_id", db.Integer, db.ForeignKey(
                              'attempts.id', ondelete="CASCADE"), nullable=False),
                          db.Column("attempt_question_id", db.Integer, db.ForeignKey(
                              'question.id', ondelete="CASCADE"), nullable=False),
                          db.Column("attempt_answer_id", db.Integer, db.ForeignKey(
                              'answer.id', ondelete="CASCADE"), nullable=False),
                          db.Column("creation_date", db.DateTime(),
                                    default=datetime.now, nullable=False),
                          db.Column("updated_date", db.DateTime(),
                                    default=datetime.now, onupdate=datetime.now, nullable=False)
                          )

attempts = db.Table("attempts",
                    db.Column("id", db.Integer,
                              primary_key=True, nullable=False),
                    db.Column("reviewer_id", db.Integer, db.ForeignKey(
                        'reviewer.id', ondelete="CASCADE"), nullable=False),
                    db.Column("user_id", db.Integer, db.ForeignKey(
                        'user.id', ondelete="CASCADE"), nullable=False),
                    db.Column("status", db.String(20), nullable=False),
                    db.Column("score", db.Integer, nullable=False, default=0),
                    db.Column("start_time", db.DateTime(),
                              default=datetime.now, nullable=False),
                    db.Column("end_time", db.DateTime(), default=datetime.now),
                    )

user_reviewers = db.Table("user-reviewers",
                          db.Column("id", db.Integer,
                                    primary_key=True, nullable=False),
                          db.Column("reviewer_id", db.Integer, db.ForeignKey(
                              'reviewer.id'), nullable=False),
                          db.Column("user_id", db.Integer, db.ForeignKey(
                              'user.id'), nullable=False),
                          db.Column("bought_date",  db.DateTime(),
                                    default=datetime.now, nullable=False)
                          )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(120), unique=True, nullable=False)
    school = db.Column(db.String(300))
    course = db.Column(db.String(60))
    profile_picture = db.Column(
        db.String(100), nullable=False, default='default.jpg')
    password = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(
        db.DateTime(), default=datetime.now, nullable=False)
    last_online = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    updated_date = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    phone = db.relationship(
        'Phone', backref='owner', lazy=True, uselist=False, passive_deletes=True)

    reviewers = db.relationship(
        'Reviewer', secondary=user_reviewers, backref='owners', lazy=True)

    attempts = db.relationship(
        'Reviewer', secondary=attempts, backref='attempts')

    def __repr__(self):
        return f"User('{self.username}','{self.reviewers}') "


class Phone(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    country_code = db.Column(db.String(10))
    phone_number = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"Phone('{self.country_code}','{self.phone_number}') "


class Message(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)
    recipient_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_type = db.Column(db.String(60), nullable=False)
    body = db.Column(db.Text, nullable=False)
    reviewer_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"Message('{self.id}','{self.recipient_id}','{self.body}')"


class Reviewer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    creation_date = db.Column(
        db.DateTime(), default=datetime.now, nullable=False)
    updated_date = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now)
    author = db.Column(db.String(80), nullable=False)
    image = db.Column(
        db.String(100), nullable=False, default='reviewer.jpg')
    details = db.Column(
        db.String(200), default="A new reviewer", nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    subjects = db.relationship(
        'Subject', backref='reviewer', passive_deletes=True)

    def __repr__(self):
        return f"Reviewer('{self.id}', '{self.name}','{self.author}') "


class Subject(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(
        db.DateTime(), default=datetime.now)
    updated_date = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now)
    name = db.Column(db.String(200), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey(
        'reviewer.id', ondelete="CASCADE"), nullable=False)
    questions = db.relationship(
        'Question', backref='reviewer', passive_deletes=True)

    def __repr__(self):
        return f"Subject('{self.id}', '{self.name}','{self.reviewer_id}') "


class Question(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(
        db.DateTime(), default=datetime.now)
    updated_date = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now)
    question = db.Column(db.String(1000), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey(
        'subject.id', ondelete="CASCADE"))
    choices = db.relationship(
        'Choice', lazy="subquery", backref='question', passive_deletes=True)
    answer = db.relationship('Answer', backref='question',
                             uselist=False, passive_deletes=True)

    def __repr__(self):
        return f"Question('{self.question}', '{self.type}','{self.choices}','{self.answer}')"


class Choice(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    creation_date = db.Column(
        db.DateTime(), default=datetime.now, nullable=False)
    updated_date = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    choice = db.Column(db.String(100), nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id', ondelete="CASCADE"), nullable=False)

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
        'question.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"Answer('{self.answer}')"

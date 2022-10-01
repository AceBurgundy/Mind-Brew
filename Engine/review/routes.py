from flask import Blueprint, render_template, redirect, url_for, jsonify
from Engine import db
from Engine.models import Reviewer, Subject

review = Blueprint('review', __name__,
                   template_folder='templates/review', static_folder='static/review')


@review.get("/start/<int:current_subject_id>")
def start(current_subject_id):

    subject = db.session.get(Subject, current_subject_id)
    if (subject.bought_test == True):
        questions = Reviewer.query.filter_by(subject_id=current_subject_id)
        return render_template('test.html', questions=questions)
    else:
        return jsonify(message="Haven't bought the test yet")

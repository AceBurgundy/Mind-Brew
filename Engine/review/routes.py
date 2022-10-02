from flask import Blueprint, render_template, redirect, url_for, jsonify
from Engine import db
from Engine.models import Test, Reviewer

review = Blueprint('review', __name__,
                   template_folder='templates/review', static_folder='static/review')


@review.get("/start/<int:current_reviewer_id>")
def start(current_reviewer_id):

    questions = Test.query.filter_by(reviewer_id=current_reviewer_id)
    return render_template('test.html', questions=questions)

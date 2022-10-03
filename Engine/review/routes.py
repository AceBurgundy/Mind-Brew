from flask import Blueprint, render_template, url_for
from Engine.models import Question
from flask_login import current_user

review = Blueprint('review', __name__,
                   template_folder='templates/review', static_folder='static/review')


@review.get("/start/<int:current_reviewer_id>")
def start(current_reviewer_id):
    """Start of test"""
    pageTitle = "Review"
    image_file = url_for(
        'static', filename='profile_pictures/' + current_user.profile_picture)

    questions = Question.query.filter_by(reviewer_id=current_reviewer_id)

    return render_template('review.html', pageTitle=pageTitle, image_file=image_file, questions=questions)

from flask import Blueprint, render_template, request, url_for, jsonify, redirect
from flask_login import current_user, login_required
from Engine.models import Subject
from Engine import mail, db
from flask_mail import Message
import os

index = Blueprint('index', __name__, template_folder='templates/index',
                  static_folder='static/index', )


@index.route("/")
@login_required
def _index():
    """Show all user projects"""
    pageTitle = "DASHBOARD"
    image_file = url_for(
        'static', filename='profile_pictures/' + current_user.profile_picture)

    if request.method == "GET":
        subjects = Subject.query.all()
        return render_template("index.html", subjects=subjects, image_file=image_file, pageTitle=pageTitle)


@index.get("/buy/<int:current_subject_id>")
def buy_test(current_subject_id):
    # buying logic
    compose = Message(current_user.username + " wants to buy a Reviewer",
                      sender=(current_user.email),
                      recipients=[os.getenv('EMAIL')]
                      )
    subject = db.session.get(Subject, current_subject_id)
    compose.body = "{name} wants to buy a reviewer for {subject_name}".format(
        name=current_user.first_name if current_user.first_name is not None else current_user.username, subject_name=subject.name)
    mail.send(compose)
    return jsonify(message="Query sent! Please contact me for a faster transaction")

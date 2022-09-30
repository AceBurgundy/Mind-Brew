from flask import Blueprint, flash, render_template, request, url_for, jsonify, redirect
from flask_login import current_user, login_required
from Engine.models import Message, Subject, User
from Engine import db
from sqlalchemy import insert
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
    subject = db.session.get(Subject, current_subject_id)

    admin = User.query.filter_by(Username=os.getenv('ADMIN')).first()

    db.session.execute(insert(Message).values(
        sender_id=current_user,
        reciepient_id=admin),
        body="{name} wants to buy a reviewer for {subject_name}".format(
        name=current_user.first_name if current_user.first_name is not None else current_user.username, subject_name=subject.name))

    db.session.commit()
    flash(f"Successfully created account.")
    return jsonify(message="Query sent! Please contact me for a faster transaction")

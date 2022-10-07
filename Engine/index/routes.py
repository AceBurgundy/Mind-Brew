from email import message
from flask import Blueprint, flash, render_template, request, url_for, jsonify, redirect
from flask_login import current_user, login_required
from Engine.models import Message, Reviewer, User, Question
from Engine import db
from sqlalchemy import insert
from Engine.helpers import addBasicData
import os

index = Blueprint('index', __name__, template_folder='templates/index',
                  static_folder='static/index', )


@index.get("/")
@login_required
def _index():
    """Show all available reviewers"""
    pageTitle = "Dashboard"
    image_file = url_for(
        'static', filename='profile_pictures/' + current_user.profile_picture)

    reviewers = Reviewer.query.all()

    # addBasicData()

    return render_template("index.html", user_reviewers=current_user.reviewers, admin=os.getenv("ADMIN"), reviewers=reviewers, image_file=image_file, pageTitle=pageTitle)


@index.get("/collection")
@login_required
def collection():
    """Show bought reviewers"""
    pageTitle = "Collection"
    image_file = url_for(
        'static', filename='profile_pictures/' + current_user.profile_picture)

    reviewers = current_user.reviewers
    return render_template("index.html", admin=os.getenv("ADMIN"), reviewers=reviewers, image_file=image_file, pageTitle=pageTitle)


@index.get("/buy/<int:current_reviewer_id>")
@login_required
def buy_test(current_reviewer_id):
    # buying logic
    reviewer = db.session.get(Reviewer, current_reviewer_id)

    admin = User.query.filter_by(username=os.getenv('ADMIN')).first()

    text = "{name} wants to buy a reviewer for {reviewer_name}".format(
        name=current_user.first_name if current_user.first_name is not None else current_user.username, reviewer_name=reviewer.name)

    db.session.execute(insert(Message).values(
        sender_id=current_user.id,
        recipient_id=admin.id,
        message_type='buy',
        reviewer_id=current_reviewer_id,
        body=text))

    db.session.commit()
    return jsonify(message="Buy request sent! Please contact me for a faster transactio     n")


@ index.get("/messages")
@ login_required
def messages():

    messages = Message.query.filter_by(recipient_id=current_user.id).limit(10)

    return jsonify([{
        'id': message.id,
        'message': message.body,
        'sender': message.sender_id,
        'type': message.message_type,
        'body': message.body,
        'reviewer_id': message.reviewer_id
    } for message in messages])


@ index.post("/allow")
@ login_required
def allow():

    reviewer = db.session.get(Reviewer,  request.form.get("reviewer_id"))

    user = db.session.get(User, request.form.get("user_id"))

    user.reviewers.append(reviewer)

    db.session.execute(insert(Message).values(
        sender_id=current_user.id,
        recipient_id=request.form.get("user_id"),
        message_type='notification',
        body=f"You can now review {reviewer.name}"))

    db.session.execute(insert(Message).values(
        sender_id=current_user.id,
        recipient_id=current_user.id,
        message_type='notification',
        body=f"You allowed {user.username} to review {reviewer.name}"))

    message = db.session.get(Message, request.form.get("message_id"))

    db.session.delete(message)

    db.session.commit()

    return jsonify(message='Transaction completed')


@ index.post("/deny")
@ login_required
def deny():

    reviewer = db.session.get(Reviewer,  request.form["reviewer_id"])

    user = db.session.get(User, request.form["user_id"])

    db.session.execute(insert(Message).values(
        sender_id=current_user.id,
        recipient_id=request.form["user_id"],
        message_type='notification',
        body=f"You request to buy {reviewer.name} had been declined"))

    db.session.execute(insert(Message).values(
        sender_id=current_user.id,
        recipient_id=current_user.id,
        message_type='notification',
        body=f"You declined {user.username} to buy {reviewer.name}"))

    message = db.session.get(Message, request.form.get("message_id"))

    db.session.delete(message)

    db.session.commit()

    return jsonify(message='Request Denied')

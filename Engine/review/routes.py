from flask import Blueprint, jsonify, render_template, request, url_for
from sqlalchemy import insert
from Engine.models import Choice, Question, Reviewer, Subject, attempts
from flask_login import current_user
from Engine import db

review = Blueprint('review', __name__,
                   template_folder='templates/review', static_folder='static/review')

subject = {
    "Graphs / Charts / Data": [],
    "English Grammar and Correct Usage": [],
    "Vocabulary": [],
    "Idiomatic Expression": [],
    "Word Analogy and Logic Test": [],
    "Reading Comprehension Test": [],
    "Paragraph Organization Test": [],
    "Clerical Operations": [],
    "Philippine Constitution, General Information, Events": [],
    "Numerical Reasoning": []
}


class Review:
    def __init__(self):
        self.__questions_with_wrong_answers = []
        self.__score = 0
        self.__subject = {}

    def add_score(self, subject_name):
        self.__score += 1
        self.__subject[subject_name] += 1

    def reduce_score(self):
        self.__score -= 1

    def get_subject(self):
        return self.__subject

    def get_score(self):
        return self.__score

    def start_anew(self):
        self.__questions_with_wrong_answers = []
        self.__score = 0

    def get_questions_with_wrong_answers(self):
        return self.__questions_with_wrong_answers

    def append_wrong_answer(self, wrong_answer):
        self.__questions_with_wrong_answers.append(wrong_answer)


# need to add class to avoid using global variables
user_review = Review()


@review.get("/start/<int:current_reviewer_id>")
def start(current_reviewer_id):
    """Start of test"""

    pageTitle = "Review"
    image_file = url_for(
        'static', filename='profile_pictures/' + current_user.profile_picture)

    user_review.start_anew()

    subjects = Subject.query.filter_by(reviewer_id=current_reviewer_id).all()

    return render_template('review.html', reviewer_id=current_reviewer_id, pageTitle=pageTitle, image_file=image_file, subjects=subjects)


@review.post("/check")
def check():
    """ Checks each answer """
    question_type = request.form.get("question_type")

    if question_type == "multiple-choice":
        question_id = request.form.get("question_id")

        if not question_id:
            return jsonify(message="Question not found")

        choice_id = request.form.get("choice_id")

        if not choice_id:
            return jsonify(message="Answer not found")

        question = Question.query.get(question_id)

        subject = Subject.query.filter_by(id=question.subject_id).first()

        choice = Choice.query.get(choice_id)

        if question.answer.answer == choice.choice:
            user_review.add_score(subject.name)
        else:
            user_review.append_wrong_answer({
                'question': question,
                'choice': choice,
                'answer': question.answer
            })
        return jsonify("Recorded")


@review.post("/remove")
def remove_answer():
    """ Removes answer on a question """

    if request.form.get("question_type") == "multiple-choice":
        question_id = request.form.get("question_id")

        if not question_id:
            return jsonify(message="Question not found")

        choice_id = request.form.get("choice_id")

        if not choice_id:
            return jsonify(message="Answer not found")

        question = Question.query.get(question_id)

        choice = Choice.query.get(choice_id)

        if question.answer.answer == choice.choice:
            user_review.reduce_score()
        else:
            for index, question in enumerate(user_review.get_questions_with_wrong_answers()):
                if question['question'] == question:
                    del user_review.get_questions_with_wrong_answers()[index]
                    break
        return jsonify("Answer removed")


@review.get("/submit/<int:current_reviewer_id>")
def submit(current_reviewer_id):
    """ Finalizes Checking """
    pageTitle = "Review"
    image_file = url_for(
        'static', filename='profile_pictures/' + current_user.profile_picture)

    questions = user_review.get_questions_with_wrong_answers()
    score = user_review.get_score()
    score_per_subject = user_review.get_subject()
    questions_length = Reviewer.query.get(current_reviewer_id).questions
    db.session.execute(insert(attempts).values(
        reviewer_id=current_reviewer_id,
        user_id=current_user.id,
        status="Completed",
        score=score))

    return render_template("score.html", score_per_subject=score_per_subject, questions_length=questions_length, reviewer_id=current_reviewer_id, score=score, questions=questions, pageTitle=pageTitle, image_file=image_file)

from flask import Blueprint

review = Blueprint('review', __name__, template_folder='templates/review', static_folder='static/review')

from flask import Blueprint

from flask import render_template, request, url_for
from flask_login import current_user, login_required
from Engine.models import Subject

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

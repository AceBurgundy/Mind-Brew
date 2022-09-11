from flask import Blueprint

from flask import flash, redirect, render_template, request, url_for
from Engine import db
from Engine.models import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_required
from Engine.helpers import save_picture
from Engine.profile.forms import (profileForm, ChangePassword)

profile = Blueprint('profile', __name__,
                    template_folder='templates/profile', static_folder='static/profile')


@profile.get("/profile")
@login_required
def _profile():
    image_file = url_for(
        'static', filename='profile_pictures/' + current_user.profile_picture)

    return render_template("profile.html", image_file=image_file, user=db.session.get(User, current_user.id))


@profile.route("/edit", methods=["POST", "GET"])
@login_required
def edit_profile():

    form = profileForm()
    passForm = ChangePassword()
    image_file = url_for(
        'static', filename='profile_pictures/' + current_user.profile_picture)

    if request.method == "POST":
        if form.validate_on_submit():
            if form.profilePicture.data:
                current_user.profile_picture = save_picture(
                    form.profilePicture.data)

            current_user.username = form.username.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.skills = form.skills.data
            current_user.address = form.address.data
            current_user.banner = form.banner.data
            current_user.country = form.country.data
            current_user.phone = form.phone.data
            flash('Successfully updated profile')
            db.session.commit()
            return redirect(url_for('profile._profile'))
        else:
            return render_template('edit-profile.html', form=form, image_file=image_file, passForm=passForm, error=form.errors)
    else:
        image_file = url_for(
            'static', filename='profile_pictures/' + current_user.profile_picture)

        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.skills.data = current_user.skills
        form.address.data = current_user.address
        form.banner.data = current_user.banner
        form.country.data = current_user.country
        form.phone.data = current_user.phone

        return render_template("edit-profile.html", form=form, image_file=image_file, passForm=passForm)


@profile.route("/change-password", methods=["POST"])
@login_required
def changePassword():
    form = ChangePassword()

    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.password.data):
            current_user.password = generate_password_hash(
                form.newPassword.data)
            db.session.commit()

            return redirect(url_for('index._index'))
        else:
            form.form_errors.append("Passwords does not match")
            return render_template("profile.html", form.form_errors)
    else:
        return render_template("profile.html", form.form_errors)

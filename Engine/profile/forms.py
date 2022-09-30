from Engine.helpers import CheckProfanity
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from werkzeug.security import check_password_hash
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, HiddenField, TelField
from Engine.models import User
from wtforms.validators import DataRequired, Length, ValidationError


class profileForm(FlaskForm):
    submit = SubmitField('UPDATE', id="save-button")

    profilePicture = FileField('Update Profile Picture', validators=[
                               FileAllowed(['jpeg', 'png', 'jpg', 'webp'])])

    first_name = StringField('First Name', id="first-name", validators=[DataRequired(
        message="Please add your username"), Length(max=50), CheckProfanity()])

    last_name = StringField('Last Name', id="last-name", validators=[DataRequired(
        message="Please add your last name"), Length(max=50), CheckProfanity()])

    school = StringField(u'School', id="school", validators=[
        Length(max=300), CheckProfanity()])

    course = StringField('Course', id="course", validators=[Length(
        max=200, message="150 character limit"), CheckProfanity()])

    phone = TelField(
        validators=[Length(max=15, message="Accepts 15 numbers only")])


class ChangePassword(FlaskForm):
    password = PasswordField(
        id="old-password-input", validators=[DataRequired("Please input old password")])

    def validate_password(self, password):
        user = User.query.filter_by(email=current_user.email)

        if check_password_hash(user, password.data) == False:
            raise ValidationError("Password does not match database records")

    newPassword = PasswordField('Enter new Password', id="new-password-input",
                                validators=[DataRequired("PLease input new password")])

    update = SubmitField(u'UPDATE', id="new-password-update-button")


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        DataRequired(), CheckProfanity(), Length(min=0, max=140)])
    submit = SubmitField('Submit')

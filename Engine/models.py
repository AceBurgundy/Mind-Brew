import json
from time import time
from datetime import datetime
from Engine import db, login_manager
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView

"""
The function below is a callback used to reload the user object from the user ID stored in the session.
It should take the str ID of a user, and return the corresponding user object. For example:
"""


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(120), unique=True, nullable=False)
    school = db.Column(db.String(300))
    course = db.Column(db.String(60))
    phone = db.Column(db.String(15))
    profile_picture = db.Column(
        db.String(100), nullable=False, default='default.jpg')
    password = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime(), default=datetime.now)
    last_online = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now)

    subjects = db.relationship('Subject', backref='reviewer', lazy=True)

    # notifications = db.relationship('Notification', backref='user',
    #                                 lazy='dynamic')
    # messages_sent = db.relationship('Message',
    #                                 foreign_keys='Message.sender_id',
    #                                 backref='author', lazy='dynamic')
    # messages_received = db.relationship('Message',
    #                                     foreign_keys='Message.recipient_id',
    #                                     backref='recipient', lazy='dynamic')
    # last_message_read_time = db.Column(db.DateTime)

    # # this is not a column so we wont see a projects column in the User database. Instead,
    # # it runs a additional querry in the backrground to match the projects that the user has created

    def __repr__(self):
        return f"User('{self.username}','{self.subjects}') "


class Subject(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    creation_date = db.Column(db.DateTime(), default=datetime.now)
    professor = db.Column(db.String(80))
    image = db.Column(
        db.String(100), nullable=False, default='subject.jpg')
    score = db.Column(db.Integer, nullable=False, default=0)
    code = db.Column(db.String(40), nullable=False)
    available_test = db.Column(db.Boolean, nullable=False, default=True)

    students = db.Column(db.Integer, db.ForeignKey('user.id'))
    questions = db.relationship('Reviewer', backref='subject', lazy=True)

    def __repr__(self):
        return f"Subject('{self.name}','{self.professor}') "


class Reviewer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    recent_review = db.Column(
        db.DateTime(), default=datetime.now, onupdate=datetime.now)
    question = db.Text()
    choice_1 = db.Column(db.String(100), nullable=False)
    choice_2 = db.Column(db.String(100), nullable=False)
    choice_3 = db.Column(db.String(100), nullable=False)
    choice_4 = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey(
        'subject.id'), nullable=False)

    def __repr__(self):
        return f"Reviewer('{self.question}','{self.correct_answer}')"


class BufferAnswers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(100), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey(
        'reviewer.id'), nullable=False)

    def __repr__(self):
        return f"BufferAnswers('{self.answer}')"


# for sending private messages
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

# for html
# {% extends "base.html" %}
# {% import 'bootstrap/wtf.html' as wtf %}

# {% block app_content %}
#     <h1>{{ _('Send Message to %(recipient)s', recipient=recipient) }}</h1>
#     <div class="row">
#         <div class="col-md-4">
#             {{ wtf.quick_form(form) }}
#         </div>
#     </div>
# {% endblock %}

# send private message route
# from app.main.forms import MessageForm
# from app.models import Message

# # ...

# @bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
# @login_required
# def send_message(recipient):
#     user = User.query.filter_by(username=recipient).first_or_404()
#     form = MessageForm()
#     if form.validate_on_submit():
#         msg = Message(author=current_user, recipient=user,
#                       body=form.message.data)
#         db.session.add(msg)
#         db.session.commit()
#         flash(_('Your message has been sent.'))
#         return redirect(url_for('main.user', username=recipient))
#     return render_template('send_message.html', title=_('Send Message'),
#                            form=form, recipient=recipient)

# # send message link when visiting user
# {% if user != current_user %}
#                 <p>
#                     <a href="{{ url_for('main.send_message',
#                                         recipient=user.username) }}">
#                         {{ _('Send private message') }}
#                     </a>
#                 </p>
#                 {% endif %}

# view private message
# @bp.route('/messages')
# @login_required
# def messages():
#     current_user.last_message_read_time = datetime.utcnow()
#     db.session.commit()
#     page = request.args.get('page', 1, type=int)
#     messages = current_user.messages_received.order_by(
#         Message.timestamp.desc()).paginate(
#             page, current_app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('main.messages', page=messages.next_num) \
#         if messages.has_next else None
#     prev_url = url_for('main.messages', page=messages.prev_num) \
#         if messages.has_prev else None
#     return render_template('messages.html', messages=messages.items,
#                            next_url=next_url, prev_url=prev_url)

# view private message html
# {% extends "base.html" %}

# {% block app_content %}
#     <h1>{{ _('Messages') }}</h1>
#     {% for post in messages %}
#         {% include '_post.html' %}
#     {% endfor %}
#     <nav aria-label="...">
#         <ul class="pager">
#             <li class="previous{% if not prev_url %} disabled{% endif %}">
#                 <a href="{{ prev_url or '#' }}">
#                     <span aria-hidden="true">&larr;</span> {{ _('Newer messages') }}
#                 </a>
#             </li>
#             <li class="next{% if not next_url %} disabled{% endif %}">
#                 <a href="{{ next_url or '#' }}">
#                     {{ _('Older messages') }} <span aria-hidden="true">&rarr;</span>
#                 </a>
#             </li>
#         </ul>
#     </nav>
# {% endblock %}

# open messages link in navbar
#  {% if current_user.is_anonymous %}
#                     ...
#                     {% else %}
#                     <li>
#                         <a href="{{ url_for('main.messages') }}">
#                             {{ _('Messages') }}
#                         </a>
#                     </li>
#                     ...
#                     {% endif %}

# notification badge to show user current number of messages
# <li>
#                         <a href="{{ url_for('main.messages') }}">
#                             {{ _('Messages') }}
#                             {% set new_messages = current_user.new_messages() %}
#                             <span id="message_count" class="badge"
#                                   style="visibility: {% if new_messages %}visible
#                                                      {% else %}hidden {% endif %};">
#                                 {{ new_messages }}
#                             </span>
#                         </a>
#                     </li>

# script
# {% block scripts %}
#     <script>
#         // ...
#         function set_message_count(n) {
#             $('#message_count').text(n);
#             $('#message_count').css('visibility', n ? 'visible' : 'hidden');
#         }
#     </script>
# {% endblock %}


# for notifications


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

# update on adding message but now with add notifications
# @bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
# @login_required
# def send_message(recipient):
#     # ...
#     if form.validate_on_submit():
#         # ...
#         user.add_notification('unread_message_count', user.new_messages())
#         db.session.commit()
#         # ...
#     # ..

# The second place where I need to notify the user is when the user goes to the messages page, at which point the unread count goes back to zero:
# view message
# @bp.route('/messages')
# @login_required
# def messages():
#     current_user.last_message_read_time = datetime.utcnow()
#     current_user.add_notification('unread_message_count', 0)
#     db.session.commit()
#     # ...

# Now that all the notifications for users are maintained in the database, I can add a new route that the client can use to retrieve notifications for the logged in user:

# app/main/routes.py: Notifications view function.

# from app.models import Notification

# # ...

# @bp.route('/notifications')
# @login_required
# def notifications():
#     since = request.args.get('since', 0.0, type=float)
#     notifications = current_user.notifications.filter(
#         Notification.timestamp > since).order_by(Notification.timestamp.asc())
#     return jsonify([{
#         'name': n.name,
#         'data': n.get_data(),
#         'timestamp': n.timestamp
#     } for n in notifications])

# polling for notifications
# {% block scripts %}
    # <script>
    #     // ...
    #     {% if current_user.is_authenticated %}
    #     $(function() {
    #         var since = 0;
    #         setInterval(function() {
    #             $.ajax('{{ url_for('main.notifications') }}?since=' + since).done(
    #                 function(notifications) {
    #                     for (var i = 0; i < notifications.length; i++) {
    #                         if (notifications[i].name == 'unread_message_count')
    #                             set_message_count(notifications[i].data);
    #                         since = notifications[i].timestamp;
    #                     }
    #                 }
    #             );
    #         }, 10000);
    #     });
    #     {% endif %}
    # </script>

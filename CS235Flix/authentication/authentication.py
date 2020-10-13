from flask import Blueprint, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
from functools import wraps

import CS235Flix.memory_repository.abtractrepository as repo
import CS235Flix.authentication.services as services

authentication_blueprint = Blueprint('authentication_bp', __name__)

class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an uppercase letter, a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    username = StringField('Username', [DataRequired(message='A username is required'),
                                        Length(min=5, message='Your username is too short')])
    password = PasswordField('Password', [DataRequired(message='A password is required'), PasswordValid()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_not_unique = None

    if form.validate_on_submit():
        try:
            services.add_user(form.username.data, form.password.data, repo.repository_instance)
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueError:
            username_not_unique = 'The username is already taken.'
    return render_template('credentials.html', title='Register', form=form, username_error_message=username_not_unique,
                           handler_url=url_for('authentication_bp.register'))

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    password_message = user_name_message = None
    if form.validate_on_submit():
        try:
            user = services.get_user(form.username.data, repo.repository_instance)
            if services.authenticate_credentials(user['username'], form.password.data, repo.repository_instance):
                session.clear()
                session['username'] = user['username']
                return redirect(url_for('home_bp.index'))
            else:
                password_message = 'Password does not match'
        except services.UnknownUserError:
            user_name_message = 'Username not found'
    return render_template('credentials.html', title='Login', username_error_message=user_name_message,
                           password_error_message=password_message, form=form)

@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.index'))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('home_bp.login_options'))
        return view(**kwargs)
    return wrapped_view

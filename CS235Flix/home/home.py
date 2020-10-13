from flask import Blueprint, render_template
home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/')
def index():
    return render_template('home.html')

@home_blueprint.route('/login_required')
def login_options():
    return render_template('requiredlogin.html')

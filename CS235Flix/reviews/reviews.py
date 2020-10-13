from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.widgets.html5 import RangeInput
from wtforms.validators import DataRequired, Length, NumberRange

from CS235Flix.common import check_movie_exists
import CS235Flix.reviews.services as services
from CS235Flix.authentication.authentication import login_required
import CS235Flix.memory_repository.abtractrepository as repo

reviews_blueprint = Blueprint('review_bp', __name__)

class ReviewForm(FlaskForm):
    content = TextAreaField('Comment', [DataRequired(message='Comment Text is required'), Length(min=10, message='Comment must be at lease 10 characters')])
    rating = IntegerRangeField(label='Rating', validators=[DataRequired(message='Rating is required'), NumberRange(min=1, max=10)], widget=RangeInput(step=1))
    submit = SubmitField('Submit Review')

@reviews_blueprint.route('/add_review', methods=['GET', 'POST'])
@login_required
def add_review():
    form = ReviewForm()
    movie_name = request.args.get('title')
    release_date = request.args.get('date')
    if release_date and isinstance(release_date, str):
        release_date_int = int(release_date)
        if check_movie_exists(movie_name, release_date_int, repo.repository_instance):
            if form.validate_on_submit():
                username = session['username']
                services.add_review(username, movie_name, release_date_int, form.content.data, form.rating.data, repo.repository_instance)
                return redirect(f"{url_for('browse_bp.view_movie_info')}?movie_name={movie_name}&date={release_date}")
        else:
            return render_template('write_review.html', movie_found=False)
    else:
        return render_template('write_review.html', movie_found=False)
    return render_template('write_review.html', handler_url=f"{url_for('review_bp.add_review')}?title={movie_name}&date={release_date}", movie_found=True,
                           form=form, title=movie_name, release_year=release_date_int)

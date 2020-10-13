from flask import Blueprint, render_template, request, url_for, session, redirect
from os.path import join as path_join
import CS235Flix.memory_repository.abtractrepository as repo
import CS235Flix.user_profile.services as services
from CS235Flix.common import check_movie_exists
from CS235Flix.authentication.authentication import login_required

watchlist_blueprint = Blueprint('watchlist_bp', __name__)

@watchlist_blueprint.route('/view_watchlist')
@login_required
def view_watchlist():
    username = session['username']
    watchlist_dict = services.get_watchlist(username, repo.repository_instance)
    return render_template('user_profile/watchlist.html', watchlist=watchlist_dict)

@watchlist_blueprint.route('/add_to_watchlist')
@login_required
def add_movie_to_watchlist():
    title = request.args.get('title')
    release_date = request.args.get('date')
    if release_date and isinstance(release_date, str):
        release_date_int = int(release_date)
        if check_movie_exists(title, release_date_int, repo.repository_instance):
            username = session['username']
            services.add_to_watchlist(username, title, release_date_int, repo.repository_instance)
            return redirect(f"{url_for('browse_bp.view_movie_info')}?movie_name={title}&date={release_date}")
        else:
            return redirect('/')
    else:
        return redirect('/')
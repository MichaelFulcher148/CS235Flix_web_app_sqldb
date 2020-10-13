from CS235Flix.common import search_for_user, make_dict_from_movie_list
from CS235Flix.memory_repository.abtractrepository import AbstractRepository
from obj.movie import Movie

def add_to_watchlist(name, movie_title, release_year, repo: AbstractRepository):
    user = search_for_user(name, repo)
    a_movie = Movie(movie_title, release_year)
    for movie in user.watchlist:
        if movie == a_movie:
            return
    user.watchlist.add_movie(a_movie)

def get_watchlist(name, repo: AbstractRepository):
    user = search_for_user(name, repo)
    movie_list = [item for item in user.watchlist]
    if len(movie_list) > 0:
        return make_dict_from_movie_list(movie_list)
    else:
        return None

from CS235Flix.memory_repository.abtractrepository import AbstractRepository
from obj.movie import Genre, Movie

def search_for_user(username: str, repo: AbstractRepository):
    a_user = None
    for user in repo.get_users():
        if user.username == username:
            a_user = user
            break
    return a_user

def make_dict_from_movie_list(movie_list: list) -> dict:
    movie_dict = dict()
    for movie in movie_list:
        movie_dict[movie.title] = movie.release_year
    return movie_dict

def get_movies_by_genre(genre_name: str, repo: 'AbstractRepository') -> list:
    a_genre = Genre(genre_name)
    movie_list = list()
    for movie in repo.get_movies():
        if a_genre in movie.genres:
            movie_list.append(movie)
    return movie_list

def check_movie_exists(title: str, date: int, repo: 'AbstractRepository') -> bool:
    a_movie = Movie(title, date)
    for movie in repo.get_movies():
        if movie == a_movie:
            return True
    return False
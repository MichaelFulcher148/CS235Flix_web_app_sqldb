from CS235Flix.memory_repository.abtractrepository import AbstractRepository
from CS235Flix.common import make_dict_from_movie_list, get_movies_by_genre

def search_movies(search_string: str, genre_name: str, title_bool: bool, actor_bool: bool, director_bool: bool, repo: 'AbstractRepository') -> list or None:
    if genre_name != '':
        movie_list = get_movies_by_genre(genre_name, repo)
    else:
        movie_list = repo.get_movies()
    if title_bool or actor_bool or director_bool:
        matches = list()
        if title_bool:
            for movie in movie_list:
                if search_string in movie.title.lower():
                    matches.append(movie)
        if actor_bool:
            for movie in movie_list:
                for actor in movie.actors:
                    if search_string in actor.actor_full_name.lower() and movie not in matches:
                        matches.append(movie)
        if director_bool:
            for movie in movie_list:
                if search_string in movie.director.director_full_name.lower() and movie not in matches:
                    matches.append(movie)
    else:
        return make_dict_from_movie_list(movie_list)
    if len(matches) > 0:
        return make_dict_from_movie_list(matches)
    return None

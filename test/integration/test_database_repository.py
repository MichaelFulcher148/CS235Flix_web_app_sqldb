import pytest
from datetime import datetime
from obj.movie import Movie, Genre, Actor, Director, Review
from CS235Flix.memory_repository.database_repository import SqlAlchemyRepository

def test_database_repository_can_get_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    the_ropos_genre_list = repo.get_genres()
    expected_str = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Drama', 'Family', 'Fantasy',
                    'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War',
                    'Western']
    expected = [Genre(name) for name in expected_str]
    assert len(expected) == len(the_ropos_genre_list)
    for genre in the_ropos_genre_list:
        assert genre in expected

def test_repository_can_get_actors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    a_actor_list = repo.get_actors()
    expected_str_list = ['50 Cent', 'Leonardo DiCaprio', 'Joseph Gordon-Levitt', 'Ellen Page', 'Ken Watanabe', 'Rita Cortese',
                'Riz Ahmed', 'Rizwan Manji', 'Rob Corddry', 'Rob Riggle', 'Robbie Amell', 'Robert Capron',
                'Robert Carlyle', 'Robert De Niro', 'Robert Downey Jr.', 'Robert Duvall', 'Robert Hoffman',
                'Robert Knepper', 'Robert Patrick', 'Robert Pattinson', 'Robert Redford', 'O\'Shea Jackson Jr.', "Temuera Morrison"]
    expected_actors = [Actor(name) for name in expected_str_list]
    for actor in expected_actors:
        assert actor in a_actor_list

def test_repository_can_get_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    a_movie_list = repo.get_movies()
    a_movie = Movie("Moana", 2016)
    spiderman_movie = Movie("The Amazing Spider-Man", 2012)
    arrival_movie = Movie('Arrival', 2016,)
    assert a_movie in a_movie_list
    assert spiderman_movie in a_movie_list
    assert arrival_movie in a_movie_list

def test_repository_can_get_directors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    a_director_list = repo.get_directors()
    expected_director = [Director("Ridley Scott"), Director('Denis Villeneuve')]
    for director in expected_director:
        assert director in a_director_list

def test_repository_can_add_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_genre(Genre('silly'))
    the_ropos_genre_list = repo.get_genres()
    assert Genre('silly') in the_ropos_genre_list

def test_repository_wont_add_genre_that_exists(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_genre(Genre('Musical'))
    the_ropos_genre_list = repo.get_genres()
    count = 0
    for gen in the_ropos_genre_list:
        if gen == Genre('Musical'):
            count += 1
    assert count == 1


def test_repository_get_number_per_genre(session_factory, a_file_reader):
    data_from_test = dict()
    repo = SqlAlchemyRepository(session_factory)
    for movie in a_file_reader.dataset_of_movies:
        for item in movie.genres:
            if item.genre_name in data_from_test:
                data_from_test[item.genre_name] += 1
            else:
                data_from_test[item.genre_name] = 1
    for key, val in data_from_test.items():
        assert val == repo.get_size_of_genre(Genre(key))

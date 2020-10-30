import pytest
from datetime import datetime
from obj.movie import Movie, Genre, Actor, Director, Review
from obj.user import User
from CS235Flix.memory_repository.database_repository import SqlAlchemyRepository
from sqlalchemy.exc import IntegrityError

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

def test_database_repository_can_get_actors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    a_actor_list = repo.get_actors()
    expected_str_list = ['50 Cent', 'Leonardo DiCaprio', 'Joseph Gordon-Levitt', 'Ellen Page', 'Ken Watanabe', 'Rita Cortese',
                'Riz Ahmed', 'Rizwan Manji', 'Rob Corddry', 'Rob Riggle', 'Robbie Amell', 'Robert Capron',
                'Robert Carlyle', 'Robert De Niro', 'Robert Downey Jr.', 'Robert Duvall', 'Robert Hoffman',
                'Robert Knepper', 'Robert Patrick', 'Robert Pattinson', 'Robert Redford', 'O\'Shea Jackson Jr.', "Temuera Morrison"]
    expected_actors = [Actor(name) for name in expected_str_list]
    for actor in expected_actors:
        assert actor in a_actor_list

def test_database_repository_can_get_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    a_movie_list = repo.get_movies()
    a_movie = Movie("Moana", 2016)
    spiderman_movie = Movie("The Amazing Spider-Man", 2012)
    arrival_movie = Movie('Arrival', 2016,)
    assert a_movie in a_movie_list
    assert spiderman_movie in a_movie_list
    assert arrival_movie in a_movie_list

def test_database_repository_can_get_directors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    a_director_list = repo.get_directors()
    expected_director = [Director("Ridley Scott"), Director('Denis Villeneuve')]
    for director in expected_director:
        assert director in a_director_list

def test_database_repository_can_add_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    count = 0
    the_ropos_genre_list = repo.get_genres()
    for gen in the_ropos_genre_list:
        if gen == Genre('silly'):
            count += 1
    assert count == 0
    repo.add_genre(Genre('silly'))
    the_ropos_genre_list = repo.get_genres()
    assert Genre('silly') in the_ropos_genre_list

def test_database_repository_wont_add_genre_that_exists(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    count = 0
    the_ropos_genre_list = repo.get_genres()
    for gen in the_ropos_genre_list:
        if gen == Genre('Musical'):
            count += 1
    assert count == 1
    with pytest.raises(IntegrityError):
        repo.add_genre(Genre('Musical'))

def test_database_repository_get_number_per_genre(session_factory, a_file_reader):
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

def test_database_repository_get_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user_name = 'man_of_pokemon'
    user_from_db = repo.find_user(user_name)
    assert user_from_db.username == user_name

def test_database_repository_can_add_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    the_ropos_actor_list = repo.get_actors()
    count = 0
    for gen in the_ropos_actor_list:
        if gen == Actor('Sam Wastheman'):
            count += 1
    assert count == 0
    repo.add_actor(Actor('Sam Wastheman'))
    the_ropos_actor_list = repo.get_actors()
    assert Actor('Sam Wastheman') in the_ropos_actor_list

def test_database_repository_wont_add_actor_that_exists(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    the_ropos_actor_list = repo.get_actors()
    count = 0
    for gen in the_ropos_actor_list:
        if gen == Actor('Emma Stone'):
            count += 1
    assert count == 1
    with pytest.raises(IntegrityError):
        repo.add_actor(Actor('Emma Stone'))

def test_database_repository_can_add_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    the_ropos_director_list = repo.get_directors()
    count = 0
    for gen in the_ropos_director_list:
        if gen == Director('Mike Wastheman'):
            count += 1
    assert count == 0
    repo.add_director(Director('Mike Wastheman'))
    the_ropos_director_list = repo.get_directors()
    assert Director('Mike Wastheman') in the_ropos_director_list

def test_database_repository_wont_add_director_that_exists(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    the_ropos_director_list = repo.get_directors()
    count = 0
    for gen in the_ropos_director_list:
        if gen == Director('David Yates'):
            count += 1
    assert count == 1
    with pytest.raises(IntegrityError):
        repo.add_director(Director('David Yates'))

def test_database_repository_can_add_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    new_movie = Movie('Guardians of Goatboy', 1914)
    new_movie.genres = [Genre('Action'), Genre('Sci-Fi')]
    new_movie.description = 'Adventures of Space soldiers sworn to protect a boy that is also a goat.'
    new_movie.director = Director("Ben Span")
    new_movie.actors = [Actor('Chris Pratt'), Actor("Bill Clinton")]
    new_movie.runtime_minutes = 400
    the_repos_movie_list = repo.get_movies()
    count = 0
    for movie in the_repos_movie_list:
        if movie == Movie('Guardians of Goatboy', 1914):
            count += 1
    assert count == 0
    repo.add_movie(new_movie)
    the_repos_movie_list = repo.get_movies()
    count = 0
    for movie in the_repos_movie_list:
        if movie == Movie('Guardians of Goatboy', 1914):
            b_movie = movie
            count += 1
    assert count == 1
    assert b_movie.description == new_movie.description
    assert b_movie.director == new_movie.director
    assert b_movie.runtime_minutes == new_movie.runtime_minutes
    assert len(b_movie.genres) == len(new_movie.genres)
    for genre in new_movie.genres:
        assert genre in b_movie.genres
    assert len(b_movie.actors) == len(new_movie.actors)
    for actor in new_movie.actors:
        assert actor in b_movie.actors

def test_database_repository_wont_add_movie_that_exists(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    the_ropos_movie_list = repo.get_movies()
    genre_str_list = 'Action,Adventure,Biography'
    actor_str_list = 'Charlie Hunnam, Robert Pattinson, Sienna Miller, Tom Holland'
    description = 'A true-life drama, centering on British explorer Col. Percival Fawcett, who disappeared while searching for a mysterious city in the Amazon in the 1920s.'
    director_str = 'James Gray'
    a_new_movie = Movie('The Lost City of Z', 2016)
    a_new_movie.director = Director('James Gray')
    a_new_movie.runtime_minutes = 141
    count = 0
    for gen in the_ropos_movie_list:
        if gen == a_new_movie:
            count += 1
    assert count == 1
    with pytest.raises(IntegrityError):
        repo.add_movie(Movie('The Lost City of Z', 2016))
    the_ropos_movie_list = repo.get_movies()
    for gen in the_ropos_movie_list:
        if gen == Movie('The Lost City of Z', 2016):
            b_movie = gen
    genre_list = [Genre(x.strip()) for x in genre_str_list.split(',')]
    actors_list = [Actor(x.strip()) for x in actor_str_list.split(',')]
    assert b_movie.description == description
    assert b_movie.director == Director(director_str)
    assert len(b_movie.genres) == len(genre_list)
    for genre in genre_list:
        assert genre in b_movie.genres
    assert len(b_movie.actors) == len(actors_list)
    for actor in actors_list:
        assert actor in b_movie.actors

def test_database_repository_can_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    a_movie = Movie('The Lost City of Z', 2016)
    a_review = Review(a_movie, 'was alright', 7)
    a_review.user = User('mistamime', 'pbkdf2:sha256:150000$i0E7SvrW$3fcec13019d221b565cb40ddd09ec38db8dc73aa5cbda722cc9a1508bc4075cb')
    repo.add_review(a_review)
    users_from_repo = repo.get_users()
    review_found = None
    for user in users_from_repo:
        for review in user.reviews:
            if review.movie == a_movie:
                review_found = review
                break
    assert review_found.review_text == 'was alright'
    assert review_found.rating == 7

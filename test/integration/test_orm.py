from datetime import datetime
from obj.user import User
from obj.movie import Director, Genre, Actor, Movie, Review

def insert_users(db_session, user_list):
    for item in user_list:
        db_session.execute(f'INSERT INTO users (username, password) VALUES (:username, :password)',
                           {'username': item[0], 'password': item[1]})

def insert_directors(db_session, director_list):
    for item in director_list:
        db_session.execute(f"INSERT INTO directors (full_name) VALUES ('{item}')")

def insert_genres(db_session, genre_list):
    for item in genre_list:
        db_session.execute(f"INSERT INTO genres (name) VALUES ('{item}')")

def insert_actors(db_session, actor_list):
    for item in actor_list:
        db_session.execute(f"INSERT INTO actors (full_name) VALUES ('{item}')")
        
def insert_movie(db_session, title, director, genres_list, actors_list, description, release_year, movie_runtime):
    temp_str = director.strip().replace("'", "''")
    result = db_session.execute(f"SELECT id FROM directors WHERE full_name = '{temp_str}'").fetchone()
    if not result:
        db_session.execute(f"INSERT INTO directors (full_name) VALUES ('{temp_str}')")
        result = db_session.execute(f"SELECT id FROM directors WHERE full_name = '{temp_str}'").fetchone()
    # print(result)
    movie_title = title.replace("'", "''")
    movie_description = description.replace("'", "''")
    db_session.execute(
        f"INSERT INTO movies (title, release_year, description, director_id, runtime_minutes) VALUES ('{movie_title}', {release_year}, '{movie_description}', {result[0]}, {movie_runtime})")
    movie_index = db_session.execute(
        f"SELECT id FROM movies WHERE title = '{movie_title}' AND release_year = {release_year}").fetchone()
    genres = [i.strip() for i in genres_list]
    for item in genres:
        result = db_session.execute(f"SELECT id FROM genres WHERE name = '{item}'").fetchone()
        if not result:
            db_session.execute(f"INSERT INTO genres (name) VALUES ('{item}')")
            result = db_session.execute(f"SELECT id FROM genres WHERE name = '{item}'").fetchone()
        db_session.execute(f"INSERT INTO movies_genres (movie_id, genre_id) VALUES ({movie_index[0]}, {result[0]})")
    actors = [i.strip().replace("'", "''") for i in actors_list]
    for item in actors:
        result = db_session.execute(f"SELECT id FROM actors WHERE full_name = '{item}'").fetchone()
        if not result:
            db_session.execute(f"INSERT INTO actors (full_name) VALUES ('{item}')")
            result = db_session.execute(f"SELECT id FROM actors WHERE full_name = '{item}'").fetchone()
        db_session.execute(f"INSERT INTO movies_actors (movie_id, actor_id) VALUES ({movie_index[0]}, {result[0]})")

def insert_review(db_session, movie_title, movie_release_year, user_id, review_text, review_rating):
    result = db_session.execute(f"SELECT id FROM movies WHERE title = '{movie_title}' AND release_year = {movie_release_year}").fetchone()
    if result:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db_session.execute(f"INSERT INTO reviews (movie_id, review_text, rating, timestamp, user_id) VALUES ({result[0]}, '{review_text}', {review_rating}, '{timestamp}', {user_id})")
    else:
        print("insert review - Movie not found")

def test_loading_users(empty_session):
    users = list()
    users.append(("jim", '98765432'))
    users.append(('jill', 'mjydfefs'))
    insert_users(empty_session, users)
    expected = [User('Jim', '98765432'), User('Jill', 'mjydfefs')]
    assert empty_session.query(User).all() == expected

def test_load_director(empty_session):
    dirctor_list = ["Ridley Scott", 'Stephen Burg']
    insert_directors(empty_session, dirctor_list)
    expected = [Director('Ridley Scott'), Director('Stephen Burg')]
    assert empty_session.query(Director).all() == expected

def test_load_genres(empty_session):
    genre_list = ["Action", 'Tool']
    insert_genres(empty_session, genre_list)
    expected = [Genre('Action'), Genre('Tool')]
    assert empty_session.query(Genre).all() == expected

def test_load_actors(empty_session):
    genre_list = ["bent board", 'Tool begone']
    insert_actors(empty_session, genre_list)
    expected = [Actor("bent board"), Actor('Tool begone')]
    assert empty_session.query(Actor).all() == expected

def test_load_movie(empty_session):
    movie_title = 'Passengers'
    genre_list = ['Adventure', 'Drama', 'Romance']
    director = 'Morten Tyldum'
    description = 'A spacecraft traveling to a distant colony planet and transporting thousands of people has a malfunction in its sleep chambers. As a result, two passengers are awakened 90 years early.'
    actors = ['Jennifer Lawrence', 'Chris Pratt', 'Michael Sheen', 'Laurence Fishburne']
    run_time = 116
    release_year = 2016
    insert_movie(empty_session, movie_title, director, genre_list, actors, description, release_year, run_time)
    a_movie = Movie(movie_title, release_year)
    a_movie.actors = [Actor(name) for name in actors]
    a_movie.description = description
    a_movie.director = Director(director)
    a_movie.genres = [Genre(name) for name in genre_list]
    a_movie.runtime_minutes = run_time
    b_movie = empty_session.query(Movie).filter(Movie._title == 'Passengers').one()
    assert b_movie == a_movie
    assert b_movie.director == a_movie.director
    assert b_movie.runtime_minutes == a_movie.runtime_minutes
    assert a_movie.description == b_movie.description
    assert len(a_movie.actors) == len(b_movie.actors)
    assert len(a_movie.genres) == len(b_movie.genres)
    for genre in a_movie.genres:
        assert genre in b_movie.genres
    for actor in a_movie.actors:
        assert actor in b_movie.actors

def test_load_review(empty_session):
    movie_title = 'Passengers'
    genre_list = ['Adventure', 'Drama', 'Romance']
    director = 'Morten Tyldum'
    description = 'A spacecraft traveling to a distant colony planet and transporting thousands of people has a malfunction in its sleep chambers. As a result, two passengers are awakened 90 years early.'
    actors = ['Jennifer Lawrence', 'Chris Pratt', 'Michael Sheen', 'Laurence Fishburne']
    run_time = 116
    release_year = 2016
    insert_movie(empty_session, movie_title, director, genre_list, actors, description, release_year, run_time)
    a_movie = Movie(movie_title, release_year)
    a_movie.actors = [Actor(name) for name in actors]
    a_movie.description = description
    a_movie.director = Director(director)
    a_movie.genres = [Genre(name) for name in genre_list]
    a_movie.runtime_minutes = run_time
    users = list()
    users.append(("jim", '98765432'))
    users.append(('jill', 'mjydfefs'))
    insert_users(empty_session, users)
    users_expected = [User('Jim', '98765432'), User('Jill', 'mjydfefs')]
    review_text = 'was definitely a 5'
    rating = 5
    a_review = Review(a_movie, review_text, rating)
    result = empty_session.execute(f"SELECT id from users WHERE username = 'jim'").fetchone()
    insert_review(empty_session, movie_title, release_year, result[0], review_text, rating)
    # result = empty_session.execute(f"SELECT id from movies WHERE title = 'Passengers'").fetchone()
    b_review = empty_session.query(Review).filter(Review._movie == a_movie).one()
    # b_review = empty_session.query(Review).filter('_user' == result[0]).all()
    # b_review = empty_session.query(Review).all()
    # print(b_review)
    # b_review = empty_session.query(Review).filter(User == users[0]).all()
    print(b_review)
    assert b_review[0] == a_review

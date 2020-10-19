from sqlalchemy import select, inspect
from sqlalchemy.engine import Engine

# from covid.adapters.orm import metadata

def test_database_populate_inspect_table_names(session):

    # Get table information
    inspector = inspect(session)
    assert inspector.get_table_names() == ['actor_colleagues', 'actors', 'directors', 'genres', 'movies', 'movies_actors', 'movies_genres', 'reviews', 'users', 'watched_movies', 'watchlist']

def get_director_id(engine, director_name):
    connection = engine.raw_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT id, full_name FROM directors WHERE full_name = '{director_name}'")
    result = cursor.fetchall()
    connection.close()
    return result[0][0]

def test_database_populate_find_director(session):
    connection = session.raw_connection()
    cursor = connection.cursor()
    temp_str = "Gavin O''Connor"
    cursor.execute(f"SELECT id, full_name FROM directors WHERE full_name = '{temp_str}'")
    result = cursor.fetchall()
    connection.close()
    assert result[0][1] == "Gavin O\'Connor"

def test_database_populate_find_movie(session):
    director_id = get_director_id(session, 'Denis Villeneuve')
    director_id2 = get_director_id(session, 'Marc Webb')
    connection = session.raw_connection()
    cursor = connection.cursor()
    temp_str = "Arrival"
    cursor.execute(f"SELECT title, description, release_year, director_id, runtime_minutes FROM movies WHERE title = '{temp_str}'")
    result = cursor.fetchall()
    description = 'When twelve mysterious spacecraft appear around the world, linguistics professor Louise Banks is tasked with interpreting the language of the apparent alien visitors.'
    assert result[0] == ('Arrival', description, 2016, director_id, 116)
    temp_str = "The Amazing Spider-Man"
    description = "After Peter Parker is bitten by a genetically altered spider, he gains newfound, spider-like powers and ventures out to solve the mystery of his parent\'s mysterious death."
    cursor.execute(f"SELECT title, description, release_year, director_id, runtime_minutes FROM movies WHERE title = '{temp_str}'")
    result = cursor.fetchall()
    connection.close()
    assert result[0] == ('The Amazing Spider-Man', description, 2012, director_id2, 136)

def test_database_populate_genre(session):
    connection = session.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name from genres")
    result = cursor.fetchall()
    connection.close()
    expected = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Drama', 'Family', 'Fantasy',
                'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War',
                'Western']
    result_list = [i[1] for i in result]
    assert len(result_list) == len(expected)
    for item in result_list:
        assert item in expected

def test_database_populate_get_genres_of_movie(session):
    connection = session.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT genres.name FROM genres INNER JOIN movies_genres genre_lists ON genre_lists.genre_id = genres.id WHERE genre_lists.movie_id IS (SELECT id FROM movies WHERE title ='Sing')")
    result = cursor.fetchall()
    expected = ['Animation', 'Comedy', 'Family']
    result_list = [i[0] for i in result]
    assert len(result_list) == len(expected)
    for i in result_list:
        assert i in expected
    cursor.execute("SELECT genres.name FROM genres INNER JOIN movies_genres genre_lists ON genre_lists.genre_id = genres.id WHERE genre_lists.movie_id IS (SELECT id FROM movies WHERE title ='300: Rise of an Empire')")
    result = cursor.fetchall()
    connection.close()
    expected = ['Action', 'Drama', 'Fantasy']
    result_list = [i[0] for i in result]
    assert len(result_list) == len(expected)
    for i in result_list:
        assert i in expected

def test_database_populate_actor(session):
    connection = session.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, full_name FROM actors")
    result = cursor.fetchall()
    connection.close()
    expected = ['50 Cent', 'Leonardo DiCaprio', 'Joseph Gordon-Levitt', 'Ellen Page', 'Ken Watanabe', 'Rita Cortese',
                'Riz Ahmed', 'Rizwan Manji', 'Rob Corddry', 'Rob Riggle', 'Robbie Amell', 'Robert Capron',
                'Robert Carlyle', 'Robert De Niro', 'Robert Downey Jr.', 'Robert Duvall', 'Robert Hoffman',
                'Robert Knepper', 'Robert Patrick', 'Robert Pattinson', 'Robert Redford', 'O\'Shea Jackson Jr.']
    result_list = [i[1] for i in result]
    for item in expected:
        assert item in result_list

def test_database_populate_get_actors_of_movie(session):
    connection = session.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT actors.full_name FROM actors INNER JOIN movies_actors actor_lists ON actor_lists.actor_id = actors.id WHERE actor_lists.movie_id IS (SELECT id FROM movies WHERE title ='The Secret Life of Pets')")
    result = cursor.fetchall()
    expected = ['Louis C.K.', 'Eric Stonestreet', 'Kevin Hart', 'Lake Bell']
    result_list = [i[0] for i in result]
    assert len(result_list) == len(expected)
    for i in result_list:
        assert i in expected
    cursor.execute("SELECT actors.full_name FROM actors INNER JOIN movies_actors actor_lists ON actor_lists.actor_id = actors.id WHERE actor_lists.movie_id IS (SELECT id FROM movies WHERE title ='Source Code')")
    result = cursor.fetchall()
    connection.close()
    expected = ['Jake Gyllenhaal', 'Michelle Monaghan', 'Vera Farmiga', 'Jeffrey Wright']
    result_list = [i[0] for i in result]
    assert len(result_list) == len(expected)
    for i in result_list:
        assert i in expected

def test_database_populate_get_users(session):
    connection = session.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT password, time_spent_watching_movies FROM users WHERE username = 'man_of_pokemon'")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][0] == 'pbkdf2:sha256:150000$0V3YMCRC$52dcf6f404ccace075ba9f88b92bbd691a14333346c1e7217ab8553210f6f684'
    assert result[0][1] == 115

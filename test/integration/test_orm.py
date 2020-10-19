from obj.user import User
from obj.movie import Director, Genre, Actor

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




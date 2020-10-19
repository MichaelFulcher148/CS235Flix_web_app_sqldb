from os.path import join as path_join
from sqlalchemy.orm import scoped_session
from sqlalchemy.engine import Engine
from flask import _app_ctx_stack
import csv
from .abtractrepository import AbstractRepository
from file_reader.file_reader import MovieFileCSVReader, UserFileReader

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

def populate(db_engine: Engine, data_path: str):
    conn = db_engine.raw_connection()
    cursor = conn.cursor()
    # file_reader = MovieFileCSVReader(path_join(data_path, 'Data1000Movies.csv'))
    # file_reader.read_csv_file()
    with open(path_join(data_path, 'Data1000Movies.csv'), encoding='utf-8-sig') as file_data:
        reader = csv.DictReader(file_data)
        for row in reader:
            temp_str = row['Director'].strip().replace("'", "''")
            result = cursor.execute(f"SELECT id FROM directors WHERE full_name = '{temp_str}'").fetchone()
            if not result:
                cursor.execute(f"INSERT INTO directors (full_name) VALUES ('{temp_str}')")
                result = cursor.execute(f"SELECT id FROM directors WHERE full_name = '{temp_str}'").fetchone()
            # print(result)
            if row['Runtime (Minutes)'].isdigit():
                movie_runtime = int(row['Runtime (Minutes)'])
            else:
                movie_runtime = 0
            if row['Year'].isdigit():
                release_year = int(row['Year'])
            else:
                release_year = 0
            movie_title = row['Title'].replace("'", "''")
            movie_description = row['Description'].replace("'", "''")
            cursor.execute(f"INSERT INTO movies (title, release_year, description, director_id, runtime_minutes) VALUES ('{movie_title}', {release_year}, '{movie_description}', {result[0]}, {movie_runtime})")
            movie_index = cursor.execute(f"SELECT id FROM movies WHERE title = '{movie_title}' AND release_year = {release_year}").fetchone()
            genres = [i.strip() for i in row['Genre'].split(',')]
            for item in genres:
                result = cursor.execute(f"SELECT id FROM genres WHERE name = '{item}'").fetchone()
                if not result:
                    cursor.execute(f"INSERT INTO genres (name) VALUES ('{item}')")
                    result = cursor.execute(f"SELECT id FROM genres WHERE name = '{item}'").fetchone()
                cursor.execute(f"INSERT INTO movies_genres (movie_id, genre_id) VALUES ({movie_index[0]}, {result[0]})")
            actors = [i.strip().replace("'", "''") for i in row['Actors'].split(',')]
            for item in actors:
                result = cursor.execute(f"SELECT id FROM actors WHERE full_name = '{item}'").fetchone()
                if not result:
                    cursor.execute(f"INSERT INTO actors (full_name) VALUES ('{item}')")
                    result = cursor.execute(f"SELECT id FROM actors WHERE full_name = '{item}'").fetchone()
                cursor.execute(f"INSERT INTO movies_actors (movie_id, actor_id) VALUES ({movie_index[0]}, {result[0]})")
            conn.commit()
    with open(path_join(data_path, 'user_data.csv'), encoding='utf-8-sig') as file_data:
        reader = csv.DictReader(file_data)
        for row in reader:
            username = row['username'].strip()
            pass_hash = row['password_hash'].strip()
            if row['time_spent_watching_movies'].isdigit():
                time_spent = int(row['time_spent_watching_movies'].strip())
            else:
                time_spent = 0
            cursor.execute(f"INSERT INTO users (username, password, time_spent_watching_movies) VALUES ('{username}', '{pass_hash}', {time_spent})")
        conn.commit()
    conn.close()
            # cursor.execute(f"INSERT INTO movies (title, release_year, description, director_id, runtime_minutes) VALUES ()")

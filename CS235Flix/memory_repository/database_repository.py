from os.path import join as path_join
from sqlalchemy.orm import scoped_session
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from flask import _app_ctx_stack
import csv
from .abtractrepository import AbstractRepository
from obj.movie import Genre, Movie, Actor, Director
from obj.user import User

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory) -> None:
        self.__session_cm = SessionContextManager(session_factory)

    def __del__(self):
        self.__session_cm.close_current_session()

    def close_session(self):
        self.__session_cm.close_current_session()

    def reset_session(self):
        self.__session_cm.reset_session()

    def get_genres(self) -> list:
        try:
            return self.__session_cm.session.query(Genre).order_by('name').all()
        except NoResultFound:
            return None

    def get_movies(self) -> list:
        try:
            return self.__session_cm.session.query(Movie).order_by('title').all()
        except NoResultFound:
            return None

    def get_actors(self) -> list:
        try:
            return self.__session_cm.session.query(Actor).order_by('full_name').all()
        except NoResultFound:
            return None

    def get_directors(self) -> list:
        try:
            return self.__session_cm.session.query(Director).order_by('full_name').all()
        except NoResultFound:
            return None

    def get_release_years(self) -> list:
        return self.__release_years

    def add_movie(self, a_movie: 'Movie') -> None:
        self.__movies.append(a_movie)
        for genre in a_movie.genres:
            if genre not in self.__genre_pop:
                self.__genre_pop[genre] = 1
            else:
                self.__genre_pop[genre] += 1

    def get_size_of_genre(self, a_genre: 'Genre') -> int:
        return self.__session_cm.session.query(Movie).filter(a_genre).count()

    def add_genre(self, a_genre: 'Genre'):
        # self.__genres.append(a_genre)
        # if a_genre not in self.__genre_pop:
        #     self.__genre_pop[a_genre] = 0
        hh = self.__session_cm.session.query(Genre).filter('name' == a_genre.genre_name).all()
        print(f"{hh} - no found")

        with self.__session_cm as scm:
            scm.session.add(a_genre)
            scm.commit()

    def add_actor(self, a_actor: 'Actor'):
        with self.__session_cm as scm:
            scm.session.add(a_actor)
            scm.commit()

    def add_director(self, a_director: 'Director'):
        with self.__session_cm as scm:
            scm.session.add(a_director)
            scm.commit()

    def add_release_year(self, a_year: int):
        self.__release_years.append(a_year)

    def add_user(self, a_user: 'User') -> None:
        with self.__session_cm as scm:
            scm.session.add(a_user)
            scm.commit()

    def get_users(self) -> list:
        return self.__session_cm.session.query(User).all()

    def find_user(self, username: str) -> 'User' or None:
        for user in self.__session_cm.session.query(User).all():
            if user.username == username:
                return user
        return None

    def add_review(self, a_review: 'Review') -> None:
        self.__reviews.append(a_review)
        print(self.__reviews)

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

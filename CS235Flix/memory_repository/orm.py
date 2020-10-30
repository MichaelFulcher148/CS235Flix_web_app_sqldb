from sqlalchemy import (Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey)
from sqlalchemy.orm import mapper, relationship
from obj.movie import Review, Movie, Genre, Actor, Director
from obj.user import User

metadata = MetaData()

users = Table('users', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
              Column('username', String(255), unique=True, nullable=False),
              Column('password', String(255), nullable=False),
              Column('time_spent_watching_movies', Integer))

user_watched_movies = Table('watched_movies', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                            Column('user_id', ForeignKey('users.id'),),
                            Column('movie_id', ForeignKey('movies.id')))

watchlists = Table('watchlist', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('user_id', ForeignKey('users.id')),
                   Column('movie_id', ForeignKey('movies.id')))

directors = Table('directors', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('full_name', String(255), unique=True, nullable=False))

genres = Table('genres', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
               Column('name', String(255), unique=True, nullable=False))

actors = Table('actors', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
               Column('full_name', String(255), unique=True, nullable=False))

actor_colleagues = Table('actor_colleagues', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                         Column('actor_id', ForeignKey('actors.id')),
                         Column('colleague_id', ForeignKey('actors.id')))

movies = Table('movies', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
               Column('title', String(255), nullable=False),
               Column('release_year', Integer, nullable=False),
               Column('description', String(2000), nullable=False),
               Column('director_id', ForeignKey('directors.id')),
               Column('runtime_minutes', Integer, nullable=False))

actors_to_movies = Table('movies_actors', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                         Column('movie_id', ForeignKey('movies.id')),
                         Column('actor_id', ForeignKey('actors.id')))

genres_to_movies = Table('movies_genres', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                         Column('movie_id', ForeignKey('movies.id')),
                         Column('genre_id', ForeignKey('genres.id')))

reviews = Table('reviews', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                Column('movie_id', ForeignKey('movies.id')),
                Column('review_text', String(1000), nullable=False),
                Column('rating', Integer, nullable=False),
                Column('timestamp', DateTime, nullable=False),
                Column('user_id', ForeignKey('users.id')))

def map_model_to_tables():
    mapper(User, users, properties={
        '_username': users.c.username,
        '_password': users.c.password,
        '_time_spent_watching_movies_minutes': users.c.time_spent_watching_movies,
        '_reviews': relationship(Review, backref='_reviews')  # ('Review')?
    })
    mapper(Genre, genres, properties={
        '_genre_name': genres.c.name
    })
    mapper(Director, directors, properties={
        '_director_full_name': directors.c.full_name
    })
    mapper(Actor, actors, properties={
        '_actor_full_name': actors.c.full_name
    })
    mapper(Review, reviews, properties={
        '_movie': relationship(Movie, backref='_movies'),
        '_review_text': reviews.c.review_text,
        '_rating': reviews.c.rating,
        '_timestamp': reviews.c.timestamp,
        '_user': relationship(User, backref='_users')
    })
    mapper(Movie, movies, properties={
        '_title': movies.c.title,
        '_release_year': movies.c.release_year,
        '_description': movies.c.description,
        '_runtime_minutes': movies.c.runtime_minutes,
        '_director': relationship(Director, backref='_directors'),
        '_actors_list': relationship(Actor, secondary=actors_to_movies, backref='_actors'),
        '_genres_list': relationship(Genre, secondary=genres_to_movies, backref='_genres')
    })

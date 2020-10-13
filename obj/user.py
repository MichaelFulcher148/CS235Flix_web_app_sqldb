from obj.movie import Movie, Review
from obj.watchlist import WatchList

class User:
    def __init__(self, name: str, password: str) -> None:
        self.__username = name.lower().strip()
        self.__password = password
        self.__watched_movies = list()
        self.__reviews = list()
        self.__time_spent_watching_movies_minutes = int()
        self.__watch_list = WatchList()

    def __repr__(self) -> str:
        return f'<User {self.__username}>'

    def __eq__(self, other) -> bool:
        return self.__username == other.username

    def __lt__(self, other) -> bool:
        return self.__username < other.username

    def __hash__(self):
        return hash(self.username)

    @property
    def username(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def watched_movies(self) -> list:
        return self.__watched_movies

    def watch_movie(self, movie: 'Movie') -> None:
        if isinstance(movie, Movie):
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes
            self.__watched_movies.append(movie)
        else:
            raise TypeError

    def add_review(self, review: 'Review') -> None:
        if isinstance(review, Review):
            self.__reviews.append(review)
        else:
            raise TypeError

    @property
    def watchlist(self) -> WatchList:
        return self.__watch_list

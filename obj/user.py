from obj.movie import Movie, Review
from obj.watchlist import WatchList

class User:
    def __init__(self, name: str, password: str) -> None:
        self._username = name.lower().strip()
        self._password = password
        self._watched_movies = list()
        self._reviews = list()
        self._time_spent_watching_movies_minutes = int()
        self._watch_list = WatchList()

    def __repr__(self) -> str:
        return f'<User {self._username}>'

    def __eq__(self, other) -> bool:
        return self._username == other.username

    def __lt__(self, other) -> bool:
        return self._username < other.username

    def __hash__(self):
        return hash(self.username)

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self._time_spent_watching_movies_minutes

    @property
    def reviews(self) -> list:
        return self._reviews

    @property
    def watched_movies(self) -> list:
        return self._watched_movies

    def watch_movie(self, movie: 'Movie') -> None:
        if isinstance(movie, Movie):
            self._time_spent_watching_movies_minutes += movie.runtime_minutes
            self._watched_movies.append(movie)
        else:
            raise TypeError

    def add_review(self, review: 'Review') -> None:
        if isinstance(review, Review):
            self._reviews.append(review)
        else:
            raise TypeError

    @property
    def watchlist(self) -> WatchList:
        return self._watch_list

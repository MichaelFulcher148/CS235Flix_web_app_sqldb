from datetime import datetime

class Director:
    def __init__(self, name: str):
        if name == '':
            self._director_full_name = None
        else:
            self._director_full_name = name

    def __repr__(self) -> str:
        return f'<Director {self._director_full_name}>'

    def __eq__(self, other: 'Director') -> bool:
        if not isinstance(other, Director):
            return False
        return self._director_full_name == other.director_full_name

    def __lt__(self, other: 'Director') -> bool:
        if not isinstance(other, Director):
            return False
        return self._director_full_name < other.director_full_name

    def __hash__(self) -> int:
        return hash(self._director_full_name)

    @property
    def director_full_name(self) -> str:
        return self._director_full_name

class Genre:
    def __init__(self, a_name: str):
        self.genre_name = a_name

    def __repr__(self) -> str:
        return f'<Genre {self._genre_name}>'

    def __eq__(self, other: 'Genre') -> bool:
        if not isinstance(other, Genre):
            return False
        return self._genre_name == other.genre_name

    def __lt__(self, other: 'Genre') -> bool:
        if not isinstance(other, Genre):
            return False
        return self._genre_name < other.genre_name

    def __hash__(self):
        return hash(self._genre_name)

    @property
    def genre_name(self) -> str:
        return self._genre_name

    @genre_name.setter
    def genre_name(self, name: str):
        if isinstance(name, str):
            if name == '':
                self._genre_name = None
            else:
                self._genre_name = name
        else:
            raise TypeError

class Actor:
    def __init__(self, name: str):
        self._actor_full_name = name
        self._colleague_list = list()

    def __repr__(self) -> str:
        return f'<Actor {self._actor_full_name}>'

    def __eq__(self, other: 'Actor') -> bool:
        if not isinstance(other, Actor):
            return False
        return self._actor_full_name == other.actor_full_name

    def __lt__(self, other: 'Actor') -> bool:
        if not isinstance(other, Actor):
            return False
        return self._actor_full_name < other.actor_full_name

    def __hash__(self) -> int:
        return hash(self._actor_full_name)

    @property
    def actor_full_name(self) -> str:
        return self._actor_full_name

    @actor_full_name.setter
    def actor_full_name(self, name: str):
        if isinstance(name, str):
            if name == '':
                self._actor_full_name = None
            else:
                self._actor_full_name = name
        else:
            raise TypeError

    def add_actor_colleague(self, colleague: 'Actor'):
        self._colleague_list.append(colleague)

    def check_if_this_actor_worked_with(self, colleague: 'Actor') -> bool:
        for a in self._colleague_list:
            if colleague == a:
                return True
        return False

class Movie:
    def __init__(self, name: str, year: int):
        self._title = name
        self._release_year = year
        self._actors_list = list()
        self._genres_list = list()
        self._description = None
        self._director = None
        self._runtime_minutes = None

    def __repr__(self) -> str:
        return f'<Movie {self._title}, {self._release_year}>'

    def __eq__(self, other: 'Movie') -> bool:
        if isinstance(other, Movie):
            return self._title == other.title and self._release_year == other.release_year
        return False

    def __lt__(self, other: 'Movie') -> bool:
        if isinstance(other, Movie):
            if self._title < other.title:
                return True
            elif self._title == other.title:
                return self._release_year < other.release_year
        return False

    def __hash__(self) -> int:
        return hash((self._title, self._release_year))

    @property
    def release_year(self) -> int:
        return self._release_year

    @release_year.setter
    def release_year(self, year: int):
        if isinstance(year, int):
            if year >= 1900:
                self._release_year = year
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, name: str):
        if isinstance(name, str):
            self._title = name
        else:
            raise TypeError

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, text: str):
        if isinstance(text, str):
            self._description = text
        else:
            raise TypeError

    @property
    def director(self) -> Director:
        return self._director

    @director.setter
    def director(self, a_director: 'Director'):
        if isinstance(a_director, Director):
            self._director = a_director
        else:
            raise TypeError

    @property
    def actors(self) -> list:
        return self._actors_list

    @actors.setter
    def actors(self, list_of_actors: list):
        if isinstance(list_of_actors, list):
            self._actors_list = list_of_actors
        else:
            raise TypeError

    @property
    def genres(self) -> list:
        return self._genres_list

    @genres.setter
    def genres(self, list_of_genres: list):
        if isinstance(list_of_genres, list):
            self._genres_list = list_of_genres
        else:
            raise TypeError

    @property
    def runtime_minutes(self) -> int:
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, minutes: int):
        if isinstance(minutes, int) and minutes > 0:
            self._runtime_minutes = minutes
        else:
            raise ValueError

    def add_actor(self, a_actor: 'Actor'):
        if isinstance(a_actor, Actor):
            if a_actor not in self._actors_list:
                self._actors_list.append(a_actor)
        else:
            raise TypeError

    def remove_actor(self, b_actor: 'Actor'):
        if isinstance(b_actor, Actor):
            try:
                self._actors_list.pop(self._actors_list.index(b_actor))
            except ValueError:
                pass
        else:
            raise TypeError

    def add_genre(self, a_genre: 'Genre'):
        if isinstance(a_genre, Genre):
            if a_genre not in self._genres_list:
                self._genres_list.append(a_genre)
        else:
            raise TypeError

    def remove_genre(self, b_genre: 'Genre'):
        if isinstance(b_genre, Genre):
            try:
                self._genres_list.pop(self._genres_list.index(b_genre))
            except ValueError:
                pass
        else:
            raise TypeError

class Review:
    def __init__(self, movie: 'Movie', review: str, rating: int) -> None:
        self._movie_ref = movie
        self._review_text = review
        if 0 < rating < 11:
            self._rating = rating
        else:
            self._rating = None
        self._timestamp = datetime.today()
        self._author = None

    def __repr__(self):
        return f'<Review {self._movie_ref}, {self._review_text}, {self._rating}, {self._timestamp}>'

    def __eq__(self, other):
        return self._movie_ref == other.movie and self._review_text == other.review_text \
               and self._rating == other.rating and self._timestamp == other.timestamp

    @property
    def movie(self):
        return self._movie_ref

    @property
    def review_text(self):
        return self._review_text

    @property
    def rating(self):
        return self._rating

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def author(self):
        return self._author

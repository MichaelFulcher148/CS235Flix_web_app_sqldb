from datetime import datetime

class Director:
    def __init__(self, name: str):
        if name == '':
            self.__director_full_name = None
        else:
            self.__director_full_name = name

    def __repr__(self) -> str:
        return f'<Director {self.__director_full_name}>'

    def __eq__(self, other: 'Director') -> bool:
        if not isinstance(other, Director):
            return False
        return self.__director_full_name == other.director_full_name

    def __lt__(self, other: 'Director') -> bool:
        if not isinstance(other, Director):
            return False
        return self.__director_full_name < other.director_full_name

    def __hash__(self) -> int:
        return hash(self.__director_full_name)

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

class Genre:
    def __init__(self, a_name: str):
        self.genre_name = a_name

    def __repr__(self) -> str:
        return f'<Genre {self.__genre_name}>'

    def __eq__(self, other: 'Genre') -> bool:
        if not isinstance(other, Genre):
            return False
        return self.__genre_name == other.__genre_name

    def __lt__(self, other: 'Genre') -> bool:
        if not isinstance(other, Genre):
            return False
        return self.__genre_name < other.__genre_name

    def __hash__(self):
        return hash(self.__genre_name)

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    @genre_name.setter
    def genre_name(self, name: str):
        if isinstance(name, str):
            if name == '':
                self.__genre_name = None
            else:
                self.__genre_name = name
        else:
            raise TypeError

class Actor:
    def __init__(self, name: str):
        self.actor_full_name = name
        self.colleague_list = list()

    def __repr__(self) -> str:
        return f'<Actor {self.__actor_full_name}>'

    def __eq__(self, other: 'Actor') -> bool:
        if not isinstance(other, Actor):
            return False
        return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other: 'Actor') -> bool:
        if not isinstance(other, Actor):
            return False
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self) -> int:
        return hash(self.__actor_full_name)

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @actor_full_name.setter
    def actor_full_name(self, name: str):
        if isinstance(name, str):
            if name == '':
                self.__actor_full_name = None
            else:
                self.__actor_full_name = name
        else:
            raise TypeError

    def add_actor_colleague(self, colleague: 'Actor'):
        self.colleague_list.append(colleague)

    def check_if_this_actor_worked_with(self, colleague: 'Actor') -> bool:
        for a in self.colleague_list:
            if colleague == a:
                return True
        return False

class Movie:
    def __init__(self, name: str, year: int):
        self.title = name
        self.release_year = year
        self.__actors_list = list()
        self.__genres_list = list()
        self.__description = None
        self.__director = None
        self.__runtime_minutes = None

    def __repr__(self) -> str:
        return f'<Movie {self.__title}, {self.__release_year}>'

    def __eq__(self, other: 'Movie') -> bool:
        if isinstance(other, Movie):
            return self.__title == other.title and self.__release_year == other.release_year
        return False

    def __lt__(self, other: 'Movie') -> bool:
        if isinstance(other, Movie):
            if self.__title < other.title:
                return True
            elif self.__title == other.title:
                return self.__release_year < other.release_year
        return False

    def __hash__(self) -> int:
        return hash((self.__title, self.__release_year))

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, year: int):
        if isinstance(year, int):
            if year >= 1900:
                self.__release_year = year
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, name: str):
        if isinstance(name, str):
            self.__title = name
        else:
            raise TypeError

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, text: str):
        if isinstance(text, str):
            self.__description = text
        else:
            raise TypeError

    @property
    def director(self) -> Director:
        return self.__director

    @director.setter
    def director(self, a_director: 'Director'):
        if isinstance(a_director, Director):
            self.__director = a_director
        else:
            raise TypeError

    @property
    def actors(self) -> list:
        return self.__actors_list

    @actors.setter
    def actors(self, list_of_actors: list):
        if isinstance(list_of_actors, list):
            self.__actors_list = list_of_actors
        else:
            raise TypeError

    @property
    def genres(self) -> list:
        return self.__genres_list

    @genres.setter
    def genres(self, list_of_genres: list):
        if isinstance(list_of_genres, list):
            self.__genres_list = list_of_genres
        else:
            raise TypeError

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, minutes: int):
        if isinstance(minutes, int) and minutes > 0:
            self.__runtime_minutes = minutes
        else:
            raise ValueError

    def add_actor(self, a_actor: 'Actor'):
        if isinstance(a_actor, Actor):
            if a_actor not in self.__actors_list:
                self.__actors_list.append(a_actor)
        else:
            raise TypeError

    def remove_actor(self, b_actor: 'Actor'):
        if isinstance(b_actor, Actor):
            try:
                self.__actors_list.pop(self.__actors_list.index(b_actor))
            except ValueError:
                pass
        else:
            raise TypeError

    def add_genre(self, a_genre: 'Genre'):
        if isinstance(a_genre, Genre):
            if a_genre not in self.__genres_list:
                self.__genres_list.append(a_genre)
        else:
            raise TypeError

    def remove_genre(self, b_genre: 'Genre'):
        if isinstance(b_genre, Genre):
            try:
                self.__genres_list.pop(self.__genres_list.index(b_genre))
            except ValueError:
                pass
        else:
            raise TypeError

class Review:
    def __init__(self, movie: 'Movie', review: str, rating: int) -> None:
        self.__movie_ref = movie
        self.__review_text = review
        if 0 < rating < 11:
            self.__rating = rating
        else:
            self.__rating = None
        self.__timestamp = datetime.today()

    def __repr__(self):
        return f'<Review {self.__movie_ref}, {self.__review_text}, {self.__rating}, {self.__timestamp}>'

    def __eq__(self, other):
        return self.__movie_ref == other.movie and self.__review_text == other.review_text \
               and self.__rating == other.rating and self.__timestamp == other.timestamp

    @property
    def movie(self):
        return self.__movie_ref

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

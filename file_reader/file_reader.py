import csv
from obj.movie import Movie, Actor, Director, Genre
from obj.user import User

class MovieFileCSVReader:
    def __init__(self, file_name: str) -> None:
        self.__filename = file_name
        self.__dataset_of_genres = set()
        self.__dataset_of_directors = set()
        self.__dataset_of_actors = set()
        self.__dataset_of_movies = list()

    @property
    def filename(self) -> str:
        return self.__filename

    @filename.setter
    def filename(self, a_name: str) -> None:
        self.__filename = a_name

    @property
    def dataset_of_movies(self) -> list:
        return self.__dataset_of_movies

    @dataset_of_movies.setter
    def dataset_of_movies(self, a_list: list) -> None:
        self.dataset_of_movies = a_list

    @property
    def dataset_of_actors(self) -> set:
        return self.__dataset_of_actors

    @dataset_of_actors.setter
    def dataset_of_actors(self, a_list: set) -> None:
        self.__dataset_of_actors = a_list

    def add_actor(self, actor: Actor) -> None:
        if isinstance(actor, Actor):
            self.__dataset_of_actors.add(actor)
        else:
            raise TypeError

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @dataset_of_directors.setter
    def dataset_of_directors(self, a_list: set) -> None:
        self.__dataset_of_directors = a_list

    def add_director(self, director: 'Director') -> None:
        if isinstance(director, Director):
            self.__dataset_of_directors.add(director)
        else:
            raise TypeError

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres

    @dataset_of_genres.setter
    def dataset_of_genres(self, a_list: set) -> None:
        self.__dataset_of_genres = a_list

    def add_genre(self, genre: Genre) -> None:
        if isinstance(genre, Genre):
            self.__dataset_of_genres.add(genre)
        else:
            raise TypeError

    def read_csv_file(self) -> None:
        with open(self.__filename, encoding='utf-8-sig') as file_data:
            reader = csv.DictReader(file_data)
            self.__dataset_of_movies = list()
            for row in reader:
                new_movie = Movie(row['Title'], int(row['Year']))
                new_movie.description = row['Description']
                new_movie.genres = [Genre(i.strip()) for i in row['Genre'].split(',')]
                new_movie.actors = [Actor(i.strip()) for i in row['Actors'].split(',')]
                new_movie.director = Director(row['Director'].strip())
                if row['Runtime (Minutes)'].isdigit():
                    new_movie.runtime_minutes = int(row['Runtime (Minutes)'])
                self.__dataset_of_movies.append(new_movie)
                for i in new_movie.genres:
                    self.add_genre(i)
                for i in new_movie.actors:
                    self.add_actor(i)
                self.add_director(new_movie.director)

class UserFileReader:
    def __init__(self, file_name: str) -> None:
        self.__filename = file_name
        self.__data_set_of_users = list()

    def add_user(self, a_user: 'User') -> None:
        if isinstance(a_user, User):
            self.__data_set_of_users.append(a_user)
        else:
            raise TypeError

    def data_set_of_users(self) -> list:
        return self.__data_set_of_users

    def read_csv_file(self) -> None:
        with open(self.__filename, encoding='utf-8-sig') as file_data:
            reader = csv.DictReader(file_data)
            for row in reader:
                new_user = User(row['username'], row['password_hash'])
                self.add_user(new_user)

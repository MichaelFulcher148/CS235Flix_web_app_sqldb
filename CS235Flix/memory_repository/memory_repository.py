from .abtractrepository import AbstractRepository
from file_reader.file_reader import MovieFileCSVReader, UserFileReader
from os.path import join as path_join

class MemoryRepository(AbstractRepository):
    def __init__(self) -> None:
        self.__movies = list()
        self.__genres = list()
        self.__actors = list()
        self.__directors = list()
        self.__release_years = list()
        self.__genre_pop = dict()
        self.__users = list()
        self.__reviews = list()

    def get_genres(self) -> list:
        return self.__genres

    def get_movies(self) -> list:
        return self.__movies

    def get_actors(self) -> list:
        return self.__actors

    def get_directors(self) -> list:
        return self.__directors

    def get_release_years(self) -> list:
        return self.__release_years

    def add_movies(self, movie_list: list) -> None:
        for item in movie_list:
            self.add_movie(item)

    def add_movie(self, a_movie: 'Movie') -> None:
        self.__movies.append(a_movie)
        for genre in a_movie.genres:
            if genre not in self.__genre_pop:
                self.__genre_pop[genre] = 1
            else:
                self.__genre_pop[genre] += 1

    def get_size_of_genre(self, a_genre: 'Genre') -> int:
        return self.__genre_pop[a_genre]

    def add_genre(self, a_genre: 'Genre'):
        self.__genres.append(a_genre)
        if a_genre not in self.__genre_pop:
            self.__genre_pop[a_genre] = 0

    def add_actor(self, a_actor: 'Actor'):
        self.__actors.append(a_actor)

    def add_director(self, a_director: 'Director'):
        self.__directors.append(a_director)

    def add_release_year(self, a_year: int):
        self.__release_years.append(a_year)

    def tidy_up(self) -> None:
        self.__movies.sort()
        self.__directors.sort()
        self.__actors.sort()
        self.__genres.sort()
        self.__release_years.sort()

    def add_user(self, a_user: 'User') -> None:
        self.__users.append(a_user)

    def get_users(self) -> list:
        return self.__users

    def find_user(self, username: str) -> 'User' or None:
        for user in self.__users:
            if user.username == username:
                return user
        return None

    def add_review(self, a_review: 'Review') -> None:
        self.__reviews.append(a_review)

def populate(data_loc: str, repo: 'MemoryRepository') -> None:
    file_reader = MovieFileCSVReader(path_join(data_loc, 'Data1000Movies.csv'))
    file_reader.read_csv_file()

    for genre in file_reader.dataset_of_genres:
        repo.add_genre(genre)
    for movie in file_reader.dataset_of_movies:
        repo.add_movie(movie)
    for director in file_reader.dataset_of_directors:
        repo.add_director(director)
    for actor in file_reader.dataset_of_actors:
        repo.add_actor(actor)
    date_list = list()
    for movie in repo.get_movies():
        if movie.release_year not in date_list:
            date_list.append(movie.release_year)
    for release_date in date_list:
        repo.add_release_year(release_date)

    file_reader = UserFileReader(path_join(data_loc, 'user_data.csv'))
    file_reader.read_csv_file()
    for user in file_reader.data_set_of_users():
        repo.add_user(user)
    repo.tidy_up()

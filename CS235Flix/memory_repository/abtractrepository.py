import abc

repository_instance = None

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get_genres(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_directors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_size_of_genre(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self):
        raise NotImplementedError

    @abc.abstractmethod
    def tidy_up(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_user(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self):
        raise NotImplementedError

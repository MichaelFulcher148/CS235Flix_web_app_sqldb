from obj.movie import Movie

class WatchList:
    def __init__(self) -> None:
        self.__the_list = list()

    def __iter__(self) -> 'iterator':
        self.__current = 0
        return self

    def __next__(self):
        if self.__current == len(self.__the_list):
            raise StopIteration
        else:
            data = self.__the_list[self.__current]
            self.__current += 1
            return data

    def size(self) -> int:
        return len(self.__the_list)

    def first_movie_in_watchlist(self) -> 'Movie' or None:
        if len(self.__the_list) != 0:
            return self.__the_list[0]
        return None

    def add_movie(self, a_movie: 'Movie') -> None:
        if isinstance(a_movie, Movie):
            if a_movie not in self.__the_list:
                self.__the_list.append(a_movie)
        else:
            raise TypeError

    def remove_movie(self, a_movie: 'Movie') -> None:
        if isinstance(a_movie, Movie):
            try:
                num = self.__the_list.index(a_movie)
            except ValueError:
                return
            self.__the_list.pop(num)
        else:
            raise TypeError

    def select_movie_to_watch(self, num: int) -> 'Movie' or None:
        if num + 1 > len(self.__the_list):
            return None
        return self.__the_list[num]

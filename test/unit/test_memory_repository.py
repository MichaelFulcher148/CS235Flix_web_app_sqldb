from obj.movie import Movie, Genre, Actor, Director

def test_repository_can_get_genres(a_memory_repo):
    a_genre_list = a_memory_repo.get_genres()
    a_genre = Genre("Action")
    assert a_genre in a_genre_list

def test_repository_can_get_actors(a_memory_repo):
    a_actor_list = a_memory_repo.get_actors()
    a_actor = Actor("Temuera Morrison")
    assert a_actor in a_actor_list

def test_repository_can_get_movies(a_memory_repo):
    a_movie_list = a_memory_repo.get_movies()
    a_movie = Movie("Moana", 2016)
    assert a_movie in a_movie_list

def test_repository_can_get_directors(a_memory_repo):
    a_director_list = a_memory_repo.get_directors()
    a_director = Director("Ridley Scott")
    assert a_director in a_director_list

def test_repository_get_number_per_genre(a_memory_repo, a_file_reader):
    data_from_test = dict()
    for movie in a_file_reader.dataset_of_movies:
        for item in movie.genres:
            if item.genre_name in data_from_test:
                data_from_test[item.genre_name] += 1
            else:
                data_from_test[item.genre_name] = 1
    for key, val in data_from_test.items():
        assert val == a_memory_repo.get_size_of_genre(Genre(key))

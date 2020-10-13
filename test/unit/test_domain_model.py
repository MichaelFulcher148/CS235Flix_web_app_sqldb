import pytest
from datetime import datetime
from obj.movie import Director, Actor, Genre, Movie, Review
from obj.watchlist import WatchList
from obj.user import User

def test_create_Director():
    burg = Director('Stephen burg')
    assert burg.__repr__() == f'<Director Stephen burg>'

def test_compare_Director():
    burg = Director('Stephen burg')
    director = Director('Stephen burg')
    director2 = Director('Tom')
    assert (burg == director) == True
    assert (director2 == director) == False

def test_create_Actor():
    cofner = Actor('Cevin Cofner')
    assert cofner.__repr__() == f'<Actor Cevin Cofner>'

def test_create_Genre():
    action = Genre('Action')
    assert action.__repr__() == f'<Genre Action>'

def test_create_Movie():
    movie = Movie("Moana", 2016)
    assert movie.title == 'Moana'
    assert movie.release_year == 2016
    assert movie.__repr__() == f'<Movie Moana, 2016>'
    ##assert movie.__hash__() == -5820196721283855152

def test_compare_Movie():
    movie = Movie("Moana", 2016)
    movie2 = Movie("Moana", 2016)
    movie3 = Movie("Lethal Weapon", 1985)
    movie4 = Movie("Lethal Bandanna", 1985)
    movie5 = Movie("Moanb", 2016)
    assert (movie == movie2) == True
    assert (movie == movie3) == False
    assert (movie3 == movie4) == False
    assert (movie5 == movie2) == False

def test_compare_lt_Movie():
    movie = Movie("Moana", 2016)
    movie2 = Movie("Moana", 2016)
    movie3 = Movie("Lethal Weapon", 1985)
    movie4 = Movie("Lethal Bandanna", 1985)
    movie5 = Movie("Moanb", 2016)
    movie6 = Movie("Moanb", 2018)
    assert (movie < movie2) == False
    assert (movie < movie3) == False
    assert (movie3 < movie) == True
    assert (movie3 < movie4) == False
    assert (movie5 < movie2) == False
    assert (movie2 < movie5) == True
    assert (movie5 < movie6) == True

def test_add_director():
    direc = Director("John Candy")
    movie = Movie("Moana", 2016)
    movie.director = direc
    assert movie.director.__repr__() == f'<Director John Candy>'

def test_change_release_year():
    movie = Movie("Moana", 2016)
    movie.release_year = 1902
    assert movie.release_year == 1902
    with pytest.raises(ValueError):
        movie.release_year = 1830
    with pytest.raises(TypeError):
        movie.release_year = '1830'

def test_change_title():
    movie = Movie("Moana", 2016)
    movie.title = 'The Blob'
    assert movie.title == 'The Blob'
    with pytest.raises(TypeError):
        movie.title = 1830

def test_add_actor():
    actor1 = Actor("Angelina Jolie")
    movie = Movie("Moana", 2016)
    movie.add_actor(actor1)
    assert movie.actors == [Actor("Angelina Jolie")]

def test_add_actors():
    movie = Movie("Moana", 2016)
    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    movie.actors = actors
    assert movie.actors == [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]

def test_remove_actor():
    movie = Movie("Moana", 2016)
    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    movie.actors = actors
    movie.remove_actor(Actor("Dwayne Johnson"))
    assert movie.actors == [Actor("Auli'i Cravalho"), Actor("Rachel House"), Actor("Temuera Morrison")]

def test_add_genre():
    movie = Movie("Moana", 2016)
    cartoon = Genre('Cartoon')
    movie.genres = [cartoon]
    assert movie.genres == [Genre('Cartoon')]

def test_remove_genre():
    movie = Movie("Moana", 2016)
    movie.genres = [Genre('Cartoon'), Genre('Kids'), Genre('Action')]
    movie.remove_genre(Genre('Action'))
    assert movie.genres == [Genre('Cartoon'), Genre('Kids')]

def test_add_movie_run_time():
    movie = Movie("Moana", 2016)
    movie.runtime_minutes = 107
    assert movie.runtime_minutes == 107

def test_create_review():
    movie = Movie("Moana", 2016)
    review = Review(movie, "was pretty good", 9)
    the_time = datetime.today()
    assert str(review.movie) == f'<Movie Moana, 2016>'
    assert review.rating == 9
    assert review.review_text == 'was pretty good'
    assert str(review) == '<Review <Movie Moana, 2016>, was pretty good, 9, {}>'.format(the_time)

def test_compare_reviews():
    movie = Movie("Moana", 2016)
    review = Review(movie, "was pretty good", 9)
    review2 = Review(movie, "was pretty good", 9)
    assert review.timestamp == review2.timestamp
    assert review.movie == review2.movie
    assert review.review_text == review2.review_text
    assert review.rating == review2.rating
    assert (review == review2) == True

def test_review_ratings():
    movie = Movie("Moana", 2016)
    review = Review(movie, "was pretty good", -2)
    assert review.rating == None
    review = Review(movie, "was pretty good", 11)
    assert review.rating == None
    review = Review(movie, "was pretty good", 2)
    assert review.rating == 2
    review = Review(movie, "was pretty good", 0)
    assert review.rating == None

def test_review_timestamp():
    movie = Movie("Moana", 2016)
    review = Review(movie, "was pretty good", -2)
    the_time = datetime.today()
    assert str(the_time) == str(review.timestamp)

def test_create_user():
    user = User('Mike', 'nope')
    assert str(user) == '<User mike>'

def test_compare_user():
    user = User('mike', 'nope')
    user2 = User('paul', 'nope')
    user3 = User('mike', 'nuddo')
    assert (user == user2) == False
    assert (user == user3) == True

def test_add_review_to_user():
    user = User('mike', 'nope')
    movie = Movie("Moana", 2016)
    review = Review(movie, "was pretty good", 9)
    user.add_review(review)
    assert user.reviews == [review]

def test_add_watched_movies():
    user = User('mike', 'nope')
    movie = Movie("Moana", 2016)
    movie.runtime_minutes = 88
    movie2 = Movie("Total Recall", 1989)
    movie2.runtime_minutes = 90
    total_time = movie2.runtime_minutes + movie.runtime_minutes
    user.watch_movie(movie)
    user.watch_movie(movie2)
    assert user.time_spent_watching_movies_minutes == total_time
    assert user.watched_movies == [movie, movie2]

def test_user_less_than():
    user = User('mike', 'nope')
    user2 = User('paul', 'nope')
    assert (user < user2) == True

def test_create_watch_list():
    watchlist = WatchList()
    assert (f"Size of watchlist: {watchlist.size()}") == f"Size of watchlist: 0"
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    assert str(watchlist.first_movie_in_watchlist()) == '<Movie Moana, 2016>'

def test_check_size():
    watchlist = WatchList()
    assert (f"Size of watchlist: {watchlist.size()}") == f"Size of watchlist: 0"
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    assert (f"Size of watchlist: {watchlist.size()}") == f"Size of watchlist: 3"

def test_remove_movie():
    watchlist = WatchList()
    assert (f"Size of watchlist: {watchlist.size()}") == f"Size of watchlist: 0"
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    assert str(watchlist.first_movie_in_watchlist()) == '<Movie Moana, 2016>'
    watchlist.remove_movie(Movie("Moana", 2016))
    assert (f"Size of watchlist: {watchlist.size()}") == f"Size of watchlist: 1"
    assert str(watchlist.first_movie_in_watchlist()) == '<Movie Ice Age, 2002>'

def test_select_movie():
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    assert watchlist.select_movie_to_watch(1) == Movie("Ice Age", 2002)
    assert watchlist.select_movie_to_watch(2) == Movie("Guardians of the Galaxy", 2012)
    assert watchlist.select_movie_to_watch(3) == None

def test_check_first_movie():
    watchlist = WatchList()
    assert watchlist.first_movie_in_watchlist() == None
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    assert watchlist.first_movie_in_watchlist() == Movie("Moana", 2016)

def test_iterator():
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    a_list = [Movie("Moana", 2016), Movie("Ice Age", 2002), Movie("Guardians of the Galaxy", 2012)]
    n = 0
    for i in watchlist:
        assert i == a_list[n]
        n += 1
    iter_obj = iter(watchlist)
    n = 0
    while n != len(a_list):
        assert iter_obj.__next__() == a_list[n]
        n += 1

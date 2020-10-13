import pytest
from flask import session

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Kick back and browse the movie list' in response.data

def test_redirect_for_no_login_on_review(client):
    response = client.get('/add_review?title=Popstar:%20Never%20Stop%20Never%20Stopping&date=2016')
    assert response.headers['Location'] == 'http://localhost/login_required'

def test_create_login(client):
    response_code = client.get('/register').status_code
    assert response_code == 200

    response = client.post('/register', data={'username': 'Billy Jones', 'password': 'itWasPaintedWh1te'})
    assert response.headers['Location'] == 'http://localhost/login'

@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'A username is required'),
        ('how', '', b'Your username is too short'),
        ('mista', '', b'A password is required'),
        ('mistamime', 'bulbasour', b'Your password must be at least 8 characters, and contain an uppercase letter, a lower case letter and a digit'),
        ('man_of_pokemon', 'willb3thebestthereeverWas', b'The username is already taken')
))
def test_create_login_with_invalid_credentials(client, username, password, message):
    response = client.post('/register', data={'username': username, 'password': password})
    assert message in response.data

def test_login(client, user_credential):
    status = client.get('/login').status_code
    assert status == 200

    response = user_credential.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['username'] == 'mistamime'

def test_logout(client, user_credential):
    user_credential.login()
    with client:
        client.get('/')
        assert session['username'] == 'mistamime'

    with client:
        user_credential.logout()
        assert 'username' not in session
        assert 'user_id' not in session

def test_post_a_review(client, user_credential):
    user_credential.login()
    client.post('/add_review?title=Conan%20the%20Barbarian&date=2011',
                data={'content': 'Awesome experience.',
                      'rating': 9})
    response = client.get('/movie_info?movie_name=Conan%20the%20Barbarian&date=2011')
    assert b'Awesome experience.' in response.data
    assert b'mistamime' in response.data

def test_browse_movie_by_title(client):
    response = client.get('/browse_by_title')
    assert b'(500) Days of Summer' in response.data
    response = client.get('/browse_by_title?letter=P')
    assert b'Planet Terror' in response.data

def test_browse_movie_by_actor(client):
    response = client.get('/browse_by_actor')
    assert b'50 Cent' in response.data
    response = client.get('/browse_by_actor?actor=50%20Cent')
    assert b'Escape Plan, 2013' in response.data
    response = client.get('/browse_by_actor?letter=L')
    assert b'Laura Allen' in response.data
    response = client.get('/browse_by_actor?actor=Laura%20Dern')
    assert b'The Fault in Our Stars, 2014' in response.data

def test_browse_movie_by_director(client):
    response = client.get('/browse_by_director')
    assert b'Alexi Pappas' in response.data
    response = client.get('/browse_by_director?director=Alex%20Garland')
    assert b'Ex Machina, 2014' in response.data
    response = client.get('/browse_by_director?letter=T')
    assert b'Todd Phillips' in response.data
    response = client.get('/browse_by_director?director=Todd%20Phillips')
    assert b'War Dogs, 2016' in response.data

def test_browse_movie_by_genre(client, a_file_reader):
    response = client.get('/browse_by_genre')
    for genre in a_file_reader.dataset_of_genres:
        assert genre.genre_name.encode() in response.data

def test_browse_movie_by_specific_genre(client):
    response = client.get('/browse_by_genre?genre=Biography')
    assert b'127 Hours, 2010' in response.data
    response = client.get('/browse_by_genre?genre=Biography&letter=H')
    assert b'Hands of Stone, 2016' in response.data

def test_view_movie_data(client, a_file_reader):
    for movie in a_file_reader.dataset_of_movies:
        if movie.title == 'Planet Terror' and movie.release_year == 2007:
            a_movie = movie
            break
    response = client.get('/movie_info?movie_name=Planet%20Terror&date=2007')
    assert str(a_movie.release_year).encode() in response.data
    assert a_movie.title.encode() in response.data
    assert a_movie.director.director_full_name.encode() in response.data
    assert str(a_movie.runtime_minutes).encode() in response.data
    for genre in a_movie.genres:
        assert genre.genre_name.encode() in response.data
    for actor in a_movie.actors:
        assert actor.actor_full_name.encode() in response.data
    assert a_movie.description[0:20].encode() in response.data

def test_add_to_watchlist(client, user_credential):
    user_credential.login()
    client.get('/add_to_watchlist?title=Popstar:%20Never%20Stop%20Never%20Stopping&date=2016')
    response = client.get('/view_watchlist')
    assert b'Popstar: Never Stop Never Stopping' in response.data

def test_access_watchlist_without_login(client):
    response = client.get('/view_watchlist')
    assert response.headers['Location'] == 'http://localhost/login_required'

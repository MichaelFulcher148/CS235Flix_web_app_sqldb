from werkzeug.security import generate_password_hash, check_password_hash
from CS235Flix.common import search_for_user
from obj.user import User
from CS235Flix.memory_repository.abtractrepository import AbstractRepository

class NameNotUniqueError(Exception):
    pass

class UnknownUserError(Exception):
    pass

def add_user(name: str, password: str, repo: AbstractRepository):
    user = repo.find_user(name)
    if user is not None:
        raise NameNotUniqueError
    password_hash = generate_password_hash(password)
    user = User(name, password_hash)
    repo.add_user(user)

def get_user(name: str, repo: AbstractRepository):
    user = search_for_user(name, repo)
    if user is not None:
        return {'username': user.username}
    else:
        raise UnknownUserError

def authenticate_credentials(name: str, password: str, repo: AbstractRepository):
    user = search_for_user(name, repo)
    if user:
        return check_password_hash(user.password, password)
    else:
        return False

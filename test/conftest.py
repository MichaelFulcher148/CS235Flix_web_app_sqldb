import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
import CS235Flix.memory_repository.abtractrepository as repo
from CS235Flix.memory_repository.memory_repository import MemoryRepository, populate
import CS235Flix.memory_repository.database_repository as database_repository
from CS235Flix.memory_repository.orm import metadata, map_model_to_tables
from file_reader.file_reader import MovieFileCSVReader
from CS235Flix import create_app

# TEST_DATA_PATH = path_join('test', 'data')
TEST_DATA_PATH = os.path.join("C:", os.sep, "Users", "Michael", "OneDrive", "Documents", "UoA", "COMPSCI_235", "Assignment_3", "CS235Flix_web_app_sqldb", "test", "data")
TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'

@pytest.fixture
def a_memory_repo():
    repo.repository_instance = MemoryRepository()
    populate(TEST_DATA_PATH, repo.repository_instance)
    return repo.repository_instance

@pytest.fixture
def a_file_reader():
    reader = MovieFileCSVReader(os.path.join(TEST_DATA_PATH, 'Data1000Movies.csv'))
    reader.read_csv_file()
    return reader

@pytest.fixture
def client():
    test_app = create_app({
        'TESTING': True, 'TEST_DATA_PATH': TEST_DATA_PATH, 'WTF_CSRF_ENABLED': False, 'REPOSITORY': 'memory'})
    return test_app.test_client()

class TheUser:
    def __init__(self, client):
        self.__client = client

    def login(self, username='mistamime', password='pikashu63I'):
        return self.__client.post('/login', data={'username': username, 'password': password})

    def logout(self):
        return self.__client.get('/logout')

@pytest.fixture
def user_credential(client):
    return TheUser(client)

@pytest.fixture
def empty_session():
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session():
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    clear_mappers()
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    database_repository.populate(engine, TEST_DATA_PATH)
    yield engine
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, TEST_DATA_PATH)
    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()

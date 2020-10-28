from flask import Flask
from os.path import join as path_join
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool
import CS235Flix.memory_repository.abtractrepository as repo
from CS235Flix.memory_repository.memory_repository import MemoryRepository, populate
from CS235Flix.memory_repository import database_repository
from CS235Flix.memory_repository.orm import metadata, map_model_to_tables

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    data_path = path_join('CS235Flix', 'memory_repository')
    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
    if app.config['REPOSITORY'] == 'memory':
        repo.repository_instance = MemoryRepository()
        populate(data_path, repo.repository_instance)
    elif app.config['REPOSITORY'] == 'database':
        database_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], connect_args={"check_same_thread": False}, poolclass=NullPool, echo=app.config['SQLALCHEMY_ECHO'])
        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE")
            clear_mappers()
            metadata.create_all(database_engine)
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())
            map_model_to_tables()
            database_repository.populate(database_engine, data_path)
        else:
            map_model_to_tables()
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repository_instance = database_repository.SqlAlchemyRepository(session_factory)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .browsing import browse_by
        app.register_blueprint(browse_by.browse_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .reviews import reviews
        app.register_blueprint(reviews.reviews_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

        from .user_profile import watchlist
        app.register_blueprint(watchlist.watchlist_blueprint)

        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repository_instance, database_repository.SqlAlchemyRepository):
                repo.repository_instance.reset_session()

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repository_instance, database_repository.SqlAlchemyRepository):
                repo.repository_instance.close_session()

    return app

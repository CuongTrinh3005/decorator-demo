import os


# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))
CONNECTION_STR = "postgresql://admin:admin@localhost:5432/book_shop"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "cuongtq")
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = CONNECTION_STR
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Default configuration of Flask ENV is production, so we need to override it to dev here
    ENV = "dev"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = CONNECTION_STR
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Default configuration of Flask ENV is production, so we need to override it to dev
    ENV = "test"


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)

key = Config.SECRET_KEY

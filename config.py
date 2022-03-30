import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):

    DEBUG = False
    TESTING = False

    SECRET_KEY= os.getenv("SECRET")
    SESSION_COOKIE_SECURE = True
    SESSION_TYPE = "filesystem"

    SQLALCHEMY_BINDS = {"messages": "sqlite:///messages.sqlite3"}
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS= False

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):

    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):

    TESTING = True
    SESSION_COOKIE_SECURE = False

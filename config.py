import os


class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'production_uri'
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///to-do-app.db"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'testing_uri'
    TESTING = True
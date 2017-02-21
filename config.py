import os


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://kudos:password@localhost/kudos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'someSecretKey'
    SENTRY_DSN = 'someSentryDsn'
    SERVER_NAME = 'localhost:5000'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SERVER_NAME = 'mykudos.herokuapp.com'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

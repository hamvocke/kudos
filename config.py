class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://kudos:password@localhost/kudos'
    SECRET_KEY = 'someSecretKey'
    SENTRY_DSN = 'someSentryDsn'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/kudos_live'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

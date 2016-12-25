class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'postgresql://localhost/kudos_dev'
    SECRET_KEY = 'someSecretKey'
    SENTRY_DSN = 'someSentryDsn'

class ProductionConfig(Config):
    DATABASE_URI = 'postgresql://localhost/kudos_live'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite://:memory:'

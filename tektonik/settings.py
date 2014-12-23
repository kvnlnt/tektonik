class Config(object):
    SECRET_KEY = 'secret key'
    DEBUG = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../tektonik.db'
    SQLALCHEMY_ECHO = True
    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../tektonik.db'
    CACHE_TYPE = 'simple'
    SQLALCHEMY_ECHO = False


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../tektonik.test.db'


class DevConfig(Config):
    DEBUG = True

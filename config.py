import os
import logging.config


# default config
class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('CLEARDB_DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = 'mysql://bb3b44179051f6:d239bffa@us-cdbr-iron-east-04' \
                              '.cleardb.net/heroku_ec028af4a8b795d'
    SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2NzE0OTE4OCwiaWF0IjoxNDY3MTQ4NTg'

    SQLALCHEMY_DATABASE_URI = \
        'mysql://bb3b44179051f6:d239bffa@us-cdbr-iron-east-04' \
        '.cleardb.net/heroku_ec028af4a8b795d'

    SECRET_KEY = "NotSoSecret"
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
    # app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
    SQLALCHEMY_POOL_SIZE = 100


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql://bb3b44179051f6:d239bffa@us-cdbr-iron-east-04' \
                              '.cleardb.net/heroku_ec028af4a8b795d'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/ecommerce_db'


def configure_logging(logging_ini):
    """Configure logging from a file."""

    logging.config.fileConfig(logging_ini)
    logging.info("logging configured using '{0}'.".format(logging_ini))


def configure_logging_relative(logging_ini):
    """Configure logging from a relative file."""

    base_dir = os.path.dirname(__file__)
    logging_ini = os.path.join(base_dir, logging_ini)
    configure_logging(logging_ini)


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = True

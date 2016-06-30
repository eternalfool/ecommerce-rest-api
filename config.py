import os
import logging.config


# default config
class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/test_ecommerce_db'
    SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2NzE0OTE4OCwiaWF0IjoxNDY3MTQ4NTg'
    print SQLALCHEMY_DATABASE_URI


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/test_ecommerce_db'
    print "are you in it for love?"


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
